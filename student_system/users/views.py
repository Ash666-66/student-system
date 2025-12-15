from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from .forms import (
    CustomUserCreationForm, StudentProfileForm, TeacherProfileForm,
    UserUpdateForm, StudentProfileUpdateForm, TeacherProfileUpdateForm
)
from .models import User, StudentProfile, TeacherProfile


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('courses:dashboard')

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.user_type == 'admin':
            return reverse_lazy('courses:dashboard')
        elif user.user_type == 'teacher':
            return reverse_lazy('courses:dashboard')
        else:
            return reverse_lazy('courses:dashboard')


class CustomLogoutView(LogoutView):
    next_page = 'users:login'


def register_view(request):
    """用户注册视图"""
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)

        if user_form.is_valid():
            user_type = user_form.cleaned_data['user_type']

            try:
                with transaction.atomic():
                    user = user_form.save()

                    # 根据用户类型创建对应的档案
                    if user_type == 'student':
                        # 重定向到学生档案创建页面
                        return redirect('create_student_profile', user_id=user.id)
                    elif user_type == 'teacher':
                        # 重定向到教师档案创建页面
                        return redirect('create_teacher_profile', user_id=user.id)
                    elif user_type == 'admin':
                        messages.success(request, '管理员账户创建成功！请登录。')
                        return redirect('login')

            except Exception as e:
                messages.error(request, f'注册失败: {str(e)}')
        else:
            messages.error(request, '请修正表单中的错误。')
    else:
        user_form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': user_form})


def create_student_profile(request, user_id):
    """创建学生档案"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        profile_form = StudentProfileForm(request.POST)

        if profile_form.is_valid():
            try:
                with transaction.atomic():
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()

                    messages.success(request, '学生账户注册成功！请登录。')
                    return redirect('login')
            except Exception as e:
                messages.error(request, f'档案创建失败: {str(e)}')
    else:
        profile_form = StudentProfileForm()

    return render(request, 'users/create_student_profile.html', {
        'profile_form': profile_form,
        'user': user
    })


def create_teacher_profile(request, user_id):
    """创建教师档案"""
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        profile_form = TeacherProfileForm(request.POST)

        if profile_form.is_valid():
            try:
                with transaction.atomic():
                    profile = profile_form.save(commit=False)
                    profile.user = user
                    profile.save()

                    messages.success(request, '教师账户注册成功！请登录。')
                    return redirect('login')
            except Exception as e:
                messages.error(request, f'档案创建失败: {str(e)}')
    else:
        profile_form = TeacherProfileForm()

    return render(request, 'users/create_teacher_profile.html', {
        'profile_form': profile_form,
        'user': user
    })


@login_required
def profile_view(request):
    """用户档案查看"""
    user = request.user

    try:
        if user.user_type == 'student':
            profile = user.studentprofile
            template_name = 'users/student_profile.html'
        elif user.user_type == 'teacher':
            profile = user.teacherprofile
            template_name = 'users/teacher_profile.html'
        else:
            profile = None
            template_name = 'users/admin_profile.html'

        return render(request, template_name, {
            'user': user,
            'profile': profile
        })
    except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist):
        messages.error(request, '您的档案信息不完整，请联系管理员。')
        return redirect('courses:dashboard')


@login_required
def edit_profile_view(request):
    """编辑用户档案"""
    user = request.user

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)

        try:
            if user.user_type == 'student':
                profile = user.studentprofile
                profile_form = StudentProfileUpdateForm(request.POST, instance=profile)
                template_name = 'users/edit_student_profile.html'
            elif user.user_type == 'teacher':
                profile = user.teacherprofile
                profile_form = TeacherProfileUpdateForm(request.POST, instance=profile)
                template_name = 'users/edit_teacher_profile.html'
            else:
                profile_form = None
                template_name = 'users/edit_admin_profile.html'

            if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
                with transaction.atomic():
                    user_form.save()
                    if profile_form:
                        profile_form.save()

                    messages.success(request, '档案更新成功！')
                    return redirect('profile')
            else:
                messages.error(request, '请修正表单中的错误。')

        except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist):
            messages.error(request, '您的档案信息不完整，请联系管理员。')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=user)

        try:
            if user.user_type == 'student':
                profile = user.studentprofile
                profile_form = StudentProfileUpdateForm(instance=profile)
                template_name = 'users/edit_student_profile.html'
            elif user.user_type == 'teacher':
                profile = user.teacherprofile
                profile_form = TeacherProfileUpdateForm(instance=profile)
                template_name = 'users/edit_teacher_profile.html'
            else:
                profile_form = None
                template_name = 'users/edit_admin_profile.html'
        except (StudentProfile.DoesNotExist, TeacherProfile.DoesNotExist):
            profile_form = None
            template_name = 'users/edit_admin_profile.html'

    return render(request, template_name, {
        'user_form': user_form,
        'profile_form': profile_form
    })
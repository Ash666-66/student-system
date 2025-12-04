from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models

from .models import Course, CourseClass, Enrollment, Announcement
from .forms import (
    CourseForm, CourseClassForm, EnrollmentForm, StudentEnrollmentForm,
    GradeForm, AnnouncementForm
)

User = get_user_model()


class DashboardView(LoginRequiredMixin):
    """基础仪表板视图"""
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser or user.user_type == 'admin':
            return render(request, 'admin/dashboard.html', {
                'total_users': User.objects.count(),
                'total_students': User.objects.filter(user_type='student').count(),
                'total_teachers': User.objects.filter(user_type='teacher').count(),
                'total_courses': Course.objects.count(),
                'total_enrollments': Enrollment.objects.filter(status='approved').count(),
                'pending_enrollments': Enrollment.objects.filter(status='pending').count(),
            })
        elif user.user_type == 'teacher':
            return render(request, 'teacher/dashboard.html', {
                'user': user,
                'my_classes': CourseClass.objects.filter(teacher=user),
                'total_students': Enrollment.objects.filter(
                    course_class__teacher=user, status='approved'
                ).count(),
                'my_courses': Course.objects.filter(classes__teacher=user).distinct(),
            })
        else:
            return render(request, 'student/dashboard.html', {
                'user': user,
                'my_enrollments': Enrollment.objects.filter(
                    student=user, status='approved'
                ).select_related('course_class__course'),
                'available_courses': CourseClass.objects.filter(
                    current_students__lt=models.F('max_students')
                ).exclude(
                    enrollments__student=user
                ).select_related('course', 'teacher')[:10],
            })


@login_required
def dashboard_view(request):
    """仪表板视图"""
    dashboard = DashboardView()
    return dashboard.get(request)


class IsAdminMixin(UserPassesTestMixin):
    """管理员权限检查"""
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.user_type == 'admin'


class IsTeacherMixin(UserPassesTestMixin):
    """教师权限检查"""
    def test_func(self):
        return self.request.user.user_type == 'teacher'


class IsStudentMixin(UserPassesTestMixin):
    """学生权限检查"""
    def test_func(self):
        return self.request.user.user_type == 'student'


# 课程管理视图
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        queryset = Course.objects.all().order_by('-created_at')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(course_name__icontains=search) |
                models.Q(course_code__icontains=search)
            )
        return queryset


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        classes = self.object.classes.all().select_related('teacher')
        context['classes'] = classes

        # 计算统计数据
        total_capacity = sum(cls.max_students for cls in classes)
        total_enrolled = sum(cls.current_students for cls in classes)
        remaining_spots = max(0, total_capacity - total_enrolled)

        context['total_capacity'] = total_capacity
        context['total_enrolled'] = total_enrolled
        context['remaining_spots'] = remaining_spots

        return context


class CourseCreateView(LoginRequiredMixin, IsAdminMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

    def form_valid(self, form):
        messages.success(self.request, '课程创建成功！')
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, IsAdminMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')

    def form_valid(self, form):
        messages.success(self.request, '课程更新成功！')
        return super().form_valid(form)


class CourseDeleteView(LoginRequiredMixin, IsAdminMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('courses:course_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # 计算统计数据
        classes = course.classes.all()
        class_count = classes.count()
        total_enrolled = sum(cls.current_students for cls in classes)
        total_capacity = sum(cls.max_students for cls in classes)

        # 计算平均班级大小
        avg_class_size = total_enrolled / class_count if class_count > 0 else 0

        # 计算选课率
        enrollment_rate = (total_enrolled / total_capacity * 100) if total_capacity > 0 else 0

        # 风险评估
        risk_level = 'low'
        risk_message = '低风险'
        risk_color = 'success'

        if class_count > 10:
            risk_level = 'high'
            risk_message = '高风险：大量班次将被删除'
            risk_color = 'danger'
        elif class_count > 5 or total_enrolled > 50:
            risk_level = 'medium'
            risk_message = '中等风险：影响较大'
            risk_color = 'warning'
        elif total_enrolled > 0:
            risk_level = 'medium'
            risk_message = '中等风险：有学生选课记录'
            risk_color = 'warning'

        context.update({
            'class_count': class_count,
            'total_enrolled': total_enrolled,
            'total_capacity': total_capacity,
            'avg_class_size': round(avg_class_size, 1),
            'enrollment_rate': round(enrollment_rate, 1),
            'has_active_enrollments': classes.filter(current_students__gt=0).exists(),
            'risk_level': risk_level,
            'risk_message': risk_message,
            'risk_color': risk_color
        })

        return context

    def delete(self, request, *args, **kwargs):
        course = self.get_object()

        # 安全检查：验证用户权限
        if not (request.user.is_superuser or request.user.user_type == 'admin'):
            messages.error(request, '您没有权限删除课程！')
            return redirect('courses:course_detail', pk=course.pk)

        # 收集统计信息用于消息显示和安全检查
        class_count = course.classes.count()
        total_enrolled = sum(cls.current_students for cls in course.classes.all())

        # 安全检查：对于高风险操作的额外确认
        if class_count > 15 or total_enrolled > 100:
            # 检查是否进行了确认（通过POST参数）
            high_risk_confirm = request.POST.get('high_risk_confirm')
            if not high_risk_confirm:
                messages.error(request, '对于大规模删除操作，需要额外的管理员确认！')
                return redirect('courses:course_delete', pk=course.pk)

        # 记录删除操作日志
        from django.utils import timezone
        delete_info = {
            'course_code': course.course_code,
            'course_name': course.course_name,
            'deleted_by': request.user.username,
            'deleted_at': timezone.now().isoformat(),
            'class_count': class_count,
            'enrolled_students': total_enrolled
        }

        # 删除课程
        try:
            result = super().delete(request, *args, **kwargs)

            # 生成详细的成功消息
            if class_count > 0 or total_enrolled > 0:
                message_parts = [
                    f'课程 "{course.course_code} - {course.course_name}" 删除成功！'
                ]

                if class_count > 0:
                    message_parts.append(f'已删除 {class_count} 个课程班次')

                if total_enrolled > 0:
                    message_parts.append(f'已清除 {total_enrolled} 条选课记录')

                messages.success(request, ' | '.join(message_parts))
            else:
                messages.success(request, f'课程 "{course.course_code} - {course.course_name}" 删除成功！')

            return result

        except Exception as e:
            messages.error(request, f'删除课程时发生错误：{str(e)}')
            return redirect('courses:course_detail', pk=course.pk)


# 课程班次管理视图
class CourseClassListView(LoginRequiredMixin, ListView):
    model = CourseClass
    template_name = 'courses/class_list.html'
    context_object_name = 'classes'
    paginate_by = 10

    def get_queryset(self):
        queryset = CourseClass.objects.all().select_related('course', 'teacher').order_by('-created_at')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(class_code__icontains=search) |
                models.Q(course__course_name__icontains=search) |
                models.Q(teacher__username__icontains=search)
            )
        return queryset


class CourseClassDetailView(LoginRequiredMixin, DetailView):
    model = CourseClass
    template_name = 'courses/class_detail.html'
    context_object_name = 'class'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enrollments'] = self.object.enrollments.all().select_related('student')
        context['announcements'] = self.object.announcements.filter(is_active=True).order_by('-created_at')
        return context


class CourseClassCreateView(LoginRequiredMixin, IsAdminMixin, CreateView):
    model = CourseClass
    form_class = CourseClassForm
    template_name = 'courses/class_form.html'
    success_url = reverse_lazy('courses:class_list')

    def form_valid(self, form):
        messages.success(self.request, '课程班次创建成功！')
        return super().form_valid(form)


class CourseClassUpdateView(LoginRequiredMixin, IsAdminMixin, UpdateView):
    model = CourseClass
    form_class = CourseClassForm
    template_name = 'courses/class_form.html'
    success_url = reverse_lazy('courses:class_list')

    def form_valid(self, form):
        messages.success(self.request, '课程班次更新成功！')
        return super().form_valid(form)


# 选课管理视图
class EnrollmentListView(LoginRequiredMixin, ListView):
    model = Enrollment
    template_name = 'courses/enrollment_list.html'
    context_object_name = 'enrollments'
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            queryset = Enrollment.objects.all().select_related('student', 'course_class__course', 'course_class__teacher')
        elif user.user_type == 'teacher':
            queryset = Enrollment.objects.filter(
                course_class__teacher=user
            ).select_related('student', 'course_class__course')
        else:
            queryset = Enrollment.objects.filter(
                student=user
            ).select_related('course_class__course', 'course_class__teacher')

        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset.order_by('-enroll_time')


@login_required
def enroll_course_view(request, class_id):
    """学生选课"""
    if request.user.user_type != 'student':
        messages.error(request, '只有学生可以进行选课操作。')
        return redirect('class_list')

    course_class = get_object_or_404(CourseClass, id=class_id)

    # 检查是否已选过该课程
    if Enrollment.objects.filter(student=request.user, course_class=course_class).exists():
        messages.error(request, '您已经选过这门课程了。')
        return redirect('class_detail', pk=class_id)

    # 检查名额
    if course_class.is_full:
        messages.error(request, '该课程班次已满，无法选课。')
        return redirect('class_detail', pk=class_id)

    if request.method == 'POST':
        # 确保POST数据中不会意外包含student字段
        post_data = request.POST.copy()
        post_data.pop('student', None)

        form = StudentEnrollmentForm(post_data, student=request.user)
        if form.is_valid():
            with transaction.atomic():
                enrollment = form.save(commit=False)
                enrollment.student = request.user
                enrollment.course_class = course_class
                enrollment.save()

                # 更新选课人数
                course_class.current_students += 1
                course_class.save()

                messages.success(request, '选课申请已提交，请等待审核。')
                return redirect('courses:enrollment_list')
    else:
        form = StudentEnrollmentForm(student=request.user)
        form.fields['course_class'].initial = course_class.id

    return render(request, 'courses/enroll_form.html', {
        'form': form,
        'course_class': course_class
    })


@login_required
def approve_enrollment_view(request, enrollment_id):
    """审核选课申请"""
    if request.user.user_type not in ['admin', 'teacher']:
        messages.error(request, '您没有权限进行此操作。')
        return redirect('courses:enrollment_list')

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    action = request.POST.get('action')

    if action == 'approve':
        enrollment.status = 'approved'
        enrollment.approve_time = timezone.now()
        messages.success(request, '选课申请已通过。')
    elif action == 'reject':
        enrollment.status = 'rejected'
        # 如果已计算在选课人数中，需要减去
        if enrollment.course_class.current_students > 0:
            enrollment.course_class.current_students -= 1
            enrollment.course_class.save()
        messages.success(request, '选课申请已拒绝。')
    elif action == 'drop':
        enrollment.status = 'dropped'
        if enrollment.course_class.current_students > 0:
            enrollment.course_class.current_students -= 1
            enrollment.course_class.save()
        messages.success(request, '学生已退课。')

    enrollment.save()
    return redirect('courses:enrollment_list')


@login_required
def grade_enrollment_view(request, enrollment_id):
    """录入成绩"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    # 检查权限：教师只能给自己的学生录入成绩
    if (request.user.user_type == 'teacher' and enrollment.course_class.teacher != request.user) or \
       request.user.user_type == 'student':
        messages.error(request, '您没有权限进行此操作。')
        return redirect('courses:enrollment_list')

    if request.method == 'POST':
        form = GradeForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, '成绩录入成功。')
            return redirect('courses:enrollment_list')
    else:
        form = GradeForm(instance=enrollment)

    return render(request, 'courses/grade_form.html', {
        'form': form,
        'enrollment': enrollment
    })


# 用户管理视图（管理员专用）
class UserListView(LoginRequiredMixin, IsAdminMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        user_type = self.request.GET.get('user_type')
        if user_type:
            queryset = queryset.filter(user_type=user_type)
        return queryset


class UserDetailView(LoginRequiredMixin, IsAdminMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        try:
            if user.user_type == 'student':
                context['profile'] = user.studentprofile
                context['enrollments'] = Enrollment.objects.filter(
                    student=user
                ).select_related('course_class__course')
            elif user.user_type == 'teacher':
                context['profile'] = user.teacherprofile
                context['classes'] = CourseClass.objects.filter(teacher=user)
        except:
            pass
        return context


class CourseClassDeleteView(LoginRequiredMixin, IsAdminMixin, DeleteView):
    model = CourseClass
    template_name = 'courses/class_confirm_delete.html'
    success_url = reverse_lazy('courses:class_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, '课程班次删除成功！')
        return super().delete(request, *args, **kwargs)


@login_required
def class_unenroll_view(request, class_id):
    """学生申请退课"""
    if request.user.user_type != 'student':
        messages.error(request, '只有学生可以进行退课操作。')
        return redirect('class_detail', pk=class_id)

    course_class = get_object_or_404(CourseClass, id=class_id)
    enrollment = get_object_or_404(Enrollment, student=request.user, course_class=course_class)

    if enrollment.status != 'approved':
        messages.error(request, '只能退已审核通过的选课。')
        return redirect('class_detail', pk=class_id)

    if request.method == 'POST':
        enrollment.status = 'dropped'
        if course_class.current_students > 0:
            course_class.current_students -= 1
            course_class.save()
        enrollment.save()
        messages.success(request, '退课申请已提交。')
        return redirect('courses:enrollment_list')

    return render(request, 'courses/class_unenroll_confirm.html', {
        'course_class': course_class,
        'enrollment': enrollment
    })


@login_required
def enrollment_cancel_view(request, enrollment_id):
    """学生取消选课申请"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=request.user)

    if enrollment.status != 'pending':
        messages.error(request, '只能取消待审核的选课申请。')
        return redirect('courses:enrollment_list')

    if request.method == 'POST':
        course_class = enrollment.course_class
        if course_class.current_students > 0:
            course_class.current_students -= 1
            course_class.save()
        enrollment.delete()
        messages.success(request, '选课申请已取消。')
        return redirect('courses:enrollment_list')

    return render(request, 'courses/enrollment_cancel_confirm.html', {
        'enrollment': enrollment
    })


class AnnouncementCreateView(LoginRequiredMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm
    template_name = 'courses/announcement_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        class_id = self.request.GET.get('class')
        if class_id:
            try:
                course_class = CourseClass.objects.get(id=class_id)
                initial['course_class'] = course_class
            except CourseClass.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, '公告创建成功！')
        return super().form_valid(form)

    def get_success_url(self):
        if self.object.course_class:
            return reverse_lazy('courses:class_detail', kwargs={'pk': self.object.course_class.id})
        return reverse_lazy('courses:course_list')
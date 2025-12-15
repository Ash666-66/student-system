from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, TeacherProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(
        choices=[('student', '学生'), ('teacher', '教师')],  # 移除管理员选项
        required=True,
        label='用户类型',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    phone = forms.CharField(max_length=11, required=False, label='手机号', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入手机号'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入名'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请确认密码'}),
        }


class AdminUserCreationForm(UserCreationForm):
    """管理员专用的用户创建表单，包含所有用户类型选项"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,  # 包含所有用户类型
        required=True,
        label='用户类型',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    phone = forms.CharField(max_length=11, required=False, label='手机号', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入手机号'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'user_type', 'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入名'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请确认密码'}),
        }


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('student_id', 'name', 'gender', 'birth_date', 'grade', 'major', 'class_name', 'enrollment_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'enrollment_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=StudentProfile.GENDER_CHOICES)
        }


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ('teacher_id', 'name', 'gender', 'birth_date', 'department', 'title', 'hire_date')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=TeacherProfile.GENDER_CHOICES)
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入名'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入邮箱'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入手机号', 'maxlength': '11'}),
        }


class StudentProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只有在初始化时才添加空选项，避免覆盖已有选择
        if not self.instance.pk:  # 如果是新建实例
            self.fields['gender'].choices = [('', '请选择性别')] + list(StudentProfile.GENDER_CHOICES)
        else:  # 如果是编辑实例，确保显示当前值
            self.fields['gender'].choices = list(StudentProfile.GENDER_CHOICES)

    class Meta:
        model = StudentProfile
        fields = ('name', 'gender', 'birth_date', 'grade', 'major', 'class_name')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓名'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入年级'}),
            'major': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入专业'}),
            'class_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入班级'}),
        }


class TeacherProfileUpdateForm(forms.ModelForm):
    # 暂时不包含teacher_id字段以避免唯一性约束问题
    # 如果需要编辑teacher_id，应该通过管理员界面进行

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只有在初始化时才添加空选项，避免覆盖已有选择
        if not self.instance.pk:  # 如果是新建实例
            self.fields['gender'].choices = [('', '请选择性别')] + list(TeacherProfile.GENDER_CHOICES)
        else:  # 如果是编辑实例，确保显示当前值
            self.fields['gender'].choices = list(TeacherProfile.GENDER_CHOICES)

    class Meta:
        model = TeacherProfile
        fields = ('name', 'gender', 'birth_date', 'department', 'title')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入姓名'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入院系'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入职称'}),
        }
from django import forms
from django.db import models
from .models import Course, CourseClass, Enrollment, Announcement
from django.contrib.auth import get_user_model

User = get_user_model()


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('course_code', 'course_name', 'description', 'credits', 'hours',
                  'max_students', 'semester', 'academic_year')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class CourseClassForm(forms.ModelForm):
    class Meta:
        model = CourseClass
        fields = ('course', 'teacher', 'class_code', 'classroom', 'schedule', 'max_students')
        widgets = {
            'teacher': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只显示教师用户
        self.fields['teacher'].queryset = User.objects.filter(user_type='teacher')


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('student', 'course_class', 'status', 'grade', 'remarks')
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course_class': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(choices=Enrollment.STATUS_CHOICES),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 只显示学生用户
        self.fields['student'].queryset = User.objects.filter(user_type='student')


class StudentEnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('course_class', 'remarks')
        widgets = {
            'course_class': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'rows': 2, 'placeholder': '选课备注（可选）'}),
        }

    def __init__(self, *args, **kwargs):
        # 从kwargs中获取student参数，避免重复
        if 'student' in kwargs:
            self.student = kwargs.pop('student')
        else:
            self.student = None

        # 调用父类初始化，不传递student参数给ModelForm
        super().__init__(*args, **kwargs)

        # 只显示有可用名额的班次
        self.fields['course_class'].queryset = CourseClass.objects.filter(
            current_students__lt=models.F('max_students')
        )


class GradeForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ('grade', 'remarks')
        widgets = {
            'grade': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 0.01}),
            'remarks': forms.Textarea(attrs={'rows': 2}),
        }


class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ('title', 'content', 'course_class', 'is_active')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
            'course_class': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            # 教师只能选择自己的班次，管理员可以选择所有班次
            if user.user_type == 'teacher':
                self.fields['course_class'].queryset = CourseClass.objects.filter(teacher=user)
            elif user.user_type == 'admin':
                self.fields['course_class'].queryset = CourseClass.objects.all()
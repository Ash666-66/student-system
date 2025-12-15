from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, TeacherProfile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
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
        fields = ('first_name', 'last_name', 'email', 'phone')


class StudentProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ('name', 'gender', 'birth_date', 'grade', 'major', 'class_name')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=StudentProfile.GENDER_CHOICES)
        }


class TeacherProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = TeacherProfile
        fields = ('name', 'gender', 'birth_date', 'department', 'title')
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=TeacherProfile.GENDER_CHOICES)
        }
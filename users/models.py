from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """扩展用户模型"""
    USER_TYPE_CHOICES = (
        ('admin', '管理员'),
        ('teacher', '教师'),
        ('student', '学生'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student', verbose_name='用户类型')
    phone = models.CharField(max_length=11, blank=True, null=True, verbose_name='手机号')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class StudentProfile(models.Model):
    """学生档案"""
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    student_id = models.CharField(max_length=20, unique=True, verbose_name='学号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    grade = models.CharField(max_length=20, verbose_name='年级')
    major = models.CharField(max_length=50, verbose_name='专业')
    class_name = models.CharField(max_length=50, verbose_name='班级')
    enrollment_date = models.DateField(verbose_name='入学日期')

    class Meta:
        verbose_name = '学生档案'
        verbose_name_plural = '学生档案'

    def __str__(self):
        return f"{self.name} ({self.student_id})"


class TeacherProfile(models.Model):
    """教师档案"""
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name='教师编号')
    name = models.CharField(max_length=50, verbose_name='姓名')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='性别')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    department = models.CharField(max_length=50, verbose_name='所属院系')
    title = models.CharField(max_length=50, verbose_name='职称')
    hire_date = models.DateField(verbose_name='入职日期')

    class Meta:
        verbose_name = '教师档案'
        verbose_name_plural = '教师档案'

    def __str__(self):
        return f"{self.name} ({self.teacher_id})"
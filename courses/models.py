from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    """课程模型"""
    course_code = models.CharField(max_length=20, unique=True, verbose_name='课程代码')
    course_name = models.CharField(max_length=100, verbose_name='课程名称')
    description = models.TextField(blank=True, null=True, verbose_name='课程描述')
    credits = models.IntegerField(default=1, verbose_name='学分')
    hours = models.IntegerField(default=1, verbose_name='课时')
    max_students = models.IntegerField(default=50, verbose_name='最大选课人数')
    current_students = models.IntegerField(default=0, verbose_name='当前选课人数')
    semester = models.CharField(max_length=20, verbose_name='学期')
    academic_year = models.CharField(max_length=10, verbose_name='学年')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = '课程'

    def __str__(self):
        return f"{self.course_name} ({self.course_code})"

    @property
    def is_full(self):
        return self.current_students >= self.max_students

    @property
    def available_spots(self):
        return max(0, self.max_students - self.current_students)


class CourseClass(models.Model):
    """课程班次模型"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='classes', verbose_name='课程')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'}, verbose_name='授课教师')
    class_code = models.CharField(max_length=20, verbose_name='班次代码')
    classroom = models.CharField(max_length=50, verbose_name='教室')
    schedule = models.CharField(max_length=100, verbose_name='上课时间')
    max_students = models.IntegerField(default=50, verbose_name='最大选课人数')
    current_students = models.IntegerField(default=0, verbose_name='当前选课人数')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '课程班次'
        verbose_name_plural = '课程班次'
        unique_together = ['course', 'class_code']

    def __str__(self):
        return f"{self.course.course_name} - {self.class_code}"

    @property
    def is_full(self):
        return self.current_students >= self.max_students

    @property
    def available_spots(self):
        return max(0, self.max_students - self.current_students)


class Enrollment(models.Model):
    """选课记录模型"""
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('dropped', '已退课'),
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'}, verbose_name='学生')
    course_class = models.ForeignKey(CourseClass, on_delete=models.CASCADE, related_name='enrollments', verbose_name='课程班次')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='选课状态')
    enroll_time = models.DateTimeField(auto_now_add=True, verbose_name='选课时间')
    approve_time = models.DateTimeField(null=True, blank=True, verbose_name='审核时间')
    grade = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='成绩')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '选课记录'
        verbose_name_plural = '选课记录'
        unique_together = ['student', 'course_class']

    def __str__(self):
        return f"{self.student.username} - {self.course_class}"


class Announcement(models.Model):
    """公告模型"""
    title = models.CharField(max_length=200, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    author = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type__in': ['admin', 'teacher']}, verbose_name='发布者')
    course_class = models.ForeignKey(CourseClass, on_delete=models.CASCADE, null=True, blank=True, related_name='announcements', verbose_name='相关课程班次')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'

    def __str__(self):
        return self.title
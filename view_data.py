#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from users.models import User, StudentProfile, TeacherProfile
from courses.models import Course, Enrollment, Announcement

def print_separator(title):
    print("=" * 80)
    print(f" {title}")
    print("=" * 80)

def print_users():
    print_separator("用户数据 (Users)")

    users = User.objects.all()
    if not users.exists():
        print("没有用户数据")
        return

    for user in users:
        print(f"用户名: {user.username}")
        print(f"邮箱: {user.email}")
        print(f"用户类型: {user.user_type}")
        print(f"手机号: {user.phone}")
        print(f"是否为员工: {user.is_staff}")
        print(f"是否为超级用户: {user.is_superuser}")
        print(f"创建时间: {user.created_at}")
        print(f"最后更新: {user.updated_at}")
        print("-" * 40)

def print_student_profiles():
    print_separator("学生档案 (Student Profiles)")

    profiles = StudentProfile.objects.all()
    if not profiles.exists():
        print("没有学生档案数据")
        return

    for profile in profiles:
        print(f"学号: {profile.student_id}")
        print(f"姓名: {profile.name}")
        print(f"性别: {profile.get_gender_display()}")
        print(f"出生日期: {profile.birth_date}")
        print(f"年级: {profile.grade}")
        print(f"专业: {profile.major}")
        print(f"班级: {profile.class_name}")
        print(f"入学日期: {profile.enrollment_date}")
        print(f"关联用户: {profile.user.username}")
        print("-" * 40)

def print_teacher_profiles():
    print_separator("教师档案 (Teacher Profiles)")

    profiles = TeacherProfile.objects.all()
    if not profiles.exists():
        print("没有教师档案数据")
        return

    for profile in profiles:
        print(f"教师编号: {profile.teacher_id}")
        print(f"姓名: {profile.name}")
        print(f"性别: {profile.get_gender_display()}")
        print(f"出生日期: {profile.birth_date}")
        print(f"所属院系: {profile.department}")
        print(f"职称: {profile.title}")
        print(f"入职日期: {profile.hire_date}")
        print(f"关联用户: {profile.user.username}")
        print("-" * 40)

def print_courses():
    print_separator("课程数据 (Courses)")

    courses = Course.objects.all()
    if not courses.exists():
        print("没有课程数据")
        return

    for course in courses:
        print(f"课程代码: {course.course_code}")
        print(f"课程名称: {course.name}")
        print(f"描述: {course.description}")
        print(f"学分: {course.credits}")
        print(f"课程类型: {course.get_course_type_display()}")
        print(f"班级: {course.course_class}")
        print(f"教师: {course.teacher}")
        print(f"容量: {course.capacity}")
        print(f"已选人数: {course.enrolled_count}")
        print(f"学期: {course.semester}")
        print(f"创建时间: {course.created_at}")
        print("-" * 40)

def print_enrollments():
    print_separator("选课记录 (Enrollments)")

    enrollments = Enrollment.objects.all()
    if not enrollments.exists():
        print("没有选课记录")
        return

    for enrollment in enrollments:
        print(f"学生: {enrollment.student}")
        print(f"课程: {enrollment.course}")
        print(f"选课时间: {enrollment.enrollment_date}")
        print(f"状态: {enrollment.get_status_display()}")
        print(f"成绩: {enrollment.grade}")
        print("-" * 40)

def print_announcements():
    print_separator("课程公告 (Announcements)")

    announcements = Announcement.objects.all()
    if not announcements.exists():
        print("没有课程公告")
        return

    for announcement in announcements:
        print(f"标题: {announcement.title}")
        print(f"内容: {announcement.content}")
        print(f"关联课程: {announcement.course}")
        print(f"发布时间: {announcement.created_at}")
        print(f"是否置顶: {announcement.is_pinned}")
        print("-" * 40)

def main():
    print("Django 学生选课管理系统 - 数据库数据查看")
    print("=" * 80)

    print_users()
    print_student_profiles()
    print_teacher_profiles()
    print_courses()
    print_enrollments()
    print_announcements()

    print("=" * 80)
    print("数据查看完成")

if __name__ == "__main__":
    main()
#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from users.models import User, StudentProfile, TeacherProfile
from courses.models import Course, Enrollment, Announcement

def main():
    print("Django 学生选课管理系统 - 数据库信息")
    print("=" * 50)

    # 统计数据
    print("【数据统计】")
    print(f"用户总数: {User.objects.count()}")
    print(f"学生档案: {StudentProfile.objects.count()}")
    print(f"教师档案: {TeacherProfile.objects.count()}")
    print(f"课程总数: {Course.objects.count()}")
    print(f"选课记录: {Enrollment.objects.count()}")
    print(f"课程公告: {Announcement.objects.count()}")

    print("\n【用户列表】")
    for user in User.objects.all():
        print(f"- {user.username} ({user.user_type}) - {user.email}")

    print("\n【学生信息】")
    for student in StudentProfile.objects.all():
        print(f"- {student.student_id} {student.name} ({student.major})")

    print("\n【教师信息】")
    for teacher in TeacherProfile.objects.all():
        print(f"- {teacher.teacher_id} {teacher.name} ({teacher.department})")

    print("\n查看完整数据请运行: python view_data.py")

if __name__ == "__main__":
    main()
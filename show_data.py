#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.db import connection
from users.models import User, StudentProfile, TeacherProfile
from courses.models import Course, Enrollment, Announcement

def show_model_counts():
    """显示各模型的记录数"""
    print("📊 数据库记录统计:")
    print(f"用户总数: {User.objects.count()}")
    print(f"学生档案: {StudentProfile.objects.count()}")
    print(f"教师档案: {TeacherProfile.objects.count()}")
    print(f"课程总数: {Course.objects.count()}")
    print(f"选课记录: {Enrollment.objects.count()}")
    print(f"课程公告: {Announcement.objects.count()}")

def show_tables():
    """显示数据库表结构"""
    print("\n🏗️ 数据库表结构:")
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(f"- {table[0]}")

def main():
    print("🎓 Django 学生选课管理系统 - 数据库查看工具")
    print("=" * 50)

    # 解析命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "users":
            os.system('python view_data.py | grep -A 40 "用户数据"')
        elif command == "students":
            os.system('python view_data.py | grep -A 40 "学生档案"')
        elif command == "teachers":
            os.system('python view_data.py | grep -A 40 "教师档案"')
        elif command == "courses":
            os.system('python view_data.py | grep -A 40 "课程数据"')
        elif command == "enrollments":
            os.system('python view_data.py | grep -A 40 "选课记录"')
        elif command == "announcements":
            os.system('python view_data.py | grep -A 40 "课程公告"')
        elif command == "tables":
            show_tables()
        elif command == "count":
            show_model_counts()
        else:
            print("❌ 未知命令")
            print_help()
    else:
        show_model_counts()
        print("\n使用 'python show_data.py <command>' 查看具体数据")
        print("可用命令: users, students, teachers, courses, enrollments, announcements, tables, count")

def print_help():
    print("\n📖 可用命令:")
    print("users       - 显示所有用户")
    print("students    - 显示学生档案")
    print("teachers    - 显示教师档案")
    print("courses     - 显示课程数据")
    print("enrollments - 显示选课记录")
    print("announcements - 显示课程公告")
    print("tables      - 显示数据库表结构")
    print("count       - 显示记录统计")

if __name__ == "__main__":
    main()
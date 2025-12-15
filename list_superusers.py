#!/usr/bin/env python
import os
import sys
import django

# 添加项目路径到 sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print("=" * 60)
print("学生管理系统 - 超级管理员列表")
print("=" * 60)

# 获取所有超级管理员
superusers = User.objects.filter(is_superuser=True)

if superusers.exists():
    print(f"找到 {superusers.count()} 个超级管理员：\n")

    for i, user in enumerate(superusers, 1):
        print(f"{i}. 用户名: {user.username}")
        print(f"   邮箱: {user.email}")
        print(f"   用户类型: {getattr(user, 'user_type', '未设置')}")
        print(f"   姓名: {user.first_name} {user.last_name}".strip() or "未设置")
        print(f"   手机号: {getattr(user, 'phone', '未设置')}")
        print(f"   超级管理员: {'是' if user.is_superuser else '否'}")
        print(f"   员工权限: {'是' if user.is_staff else '否'}")
        print(f"   激活状态: {'是' if user.is_active else '否'}")
        print(f"   创建时间: {user.date_joined.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   最后登录: {user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '从未登录'}")
        print("-" * 40)
else:
    print("没有找到任何超级管理员账户。")

print("=" * 60)
print("所有管理员账户（包括普通管理员）:")
print("=" * 60)

# 获取所有管理员用户（包括普通管理员）
admin_users = User.objects.filter(user_type='admin')

if admin_users.exists():
    print(f"找到 {admin_users.count()} 个管理员用户：\n")

    for i, user in enumerate(admin_users, 1):
        print(f"{i}. 用户名: {user.username}")
        print(f"   邮箱: {user.email}")
        print(f"   用户类型: {getattr(user, 'user_type', '未设置')}")
        print(f"   超级管理员: {'是' if user.is_superuser else '否'}")
        print(f"   员工权限: {'是' if user.is_staff else '否'}")
        print("-" * 40)
else:
    print("没有找到任何管理员用户。")

print("=" * 60)
print(f"总用户数: {User.objects.count()}")
print(f"激活用户数: {User.objects.filter(is_active=True).count()}")
print("=" * 60)
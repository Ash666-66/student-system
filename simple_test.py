#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

print("=== 检查用户数据 ===")
users = User.objects.all()
print(f"总用户数: {users.count()}")

for user in users[:5]:
    print(f"ID: {user.id}, 用户名: {user.username}, 类型: {user.user_type}")

print("\n=== 检查管理员用户 ===")
admins = User.objects.filter(user_type='admin')
print(f"管理员用户数: {admins.count()}")

for admin in admins:
    print(f"ID: {admin.id}, 用户名: {admin.username}, 超级用户: {admin.is_superuser}")

print("\n=== 检查URL解析 ===")
try:
    url = reverse('courses:user_edit', kwargs={'pk': 4})
    print(f"编辑URL: {url}")
except Exception as e:
    print(f"URL解析错误: {e}")

print("\n=== 检查用户4是否存在 ===")
try:
    user4 = User.objects.get(pk=4)
    print(f"用户4存在: {user4.username}, 类型: {user4.user_type}")
except User.DoesNotExist:
    print("用户4不存在")
except Exception as e:
    print(f"查询错误: {e}")
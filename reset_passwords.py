#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from django.contrib.auth.hashers import make_password
from users.models import User

# 重置所有用户密码为简单密码
passwords = {
    'hzy': 'admin123',
    'teacher': 'teacher123',
    'student': 'student123'
}

print("重置用户密码...")
for username, new_password in passwords.items():
    try:
        user = User.objects.get(username=username)
        user.password = make_password(new_password)
        user.save()
        print(f"用户 {username} 密码已重置为: {new_password}")
    except User.DoesNotExist:
        print(f"用户 {username} 不存在")

print("\n重置完成！现在可以使用以下账号登录:")
for username, password in passwords.items():
    print(f"  用户名: {username}, 密码: {password}")
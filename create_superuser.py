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

# 创建超级管理员账户
try:
    # 检查是否已存在用户名 hzy
    if User.objects.filter(username='hzy').exists():
        print("用户 'hzy' 已存在，正在更新...")
        user = User.objects.get(username='hzy')
        user.set_password('hzy123456')
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 'admin'
        user.save()
        print("超级管理员账户更新成功！")
    else:
        # 创建新的超级用户
        user = User.objects.create_superuser(
            username='hzy',
            email='hzy@example.com',
            password='hzy123456',
            user_type='admin'
        )
        print("超级管理员账户创建成功！")

    print("=" * 50)
    print("登录信息：")
    print("用户名: hzy")
    print("密码: hzy123456")
    print("用户类型: admin (超级管理员)")
    print("=" * 50)

except Exception as e:
    print(f"创建超级管理员账户时出错: {e}")
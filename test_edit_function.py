#!/usr/bin/env python
"""
测试用户编辑功能的脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def test_user_edit_function():
    """测试用户编辑功能"""
    print("=== 用户编辑功能测试 ===\n")

    # 创建测试客户端
    client = Client()

    # 1. 测试未登录用户访问编辑页面
    print("1. 测试未登录用户访问编辑页面:")
    try:
        response = client.get('/courses/users/4/edit/')
        print(f"   状态码: {response.status_code}")
        if response.status_code == 302:
            print(f"   重定向到: {response.url}")
            print("   ✅ 正确重定向到登录页面")
        else:
            print("   ❌ 未正确重定向")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

    # 2. 检查数据库中的用户
    print("\n2. 检查数据库中的用户:")
    try:
        users = User.objects.all()
        print(f"   总用户数: {users.count()}")
        for user in users[:5]:  # 显示前5个用户
            print(f"   - ID: {user.id}, 用户名: {user.username}, 类型: {user.user_type}, 活跃: {user.is_active}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

    # 3. 测试URL解析
    print("\n3. 测试URL解析:")
    try:
        url = reverse('courses:user_edit', kwargs={'pk': 4})
        print(f"   解析的URL: {url}")
        print("   ✅ URL解析成功")
    except Exception as e:
        print(f"   ❌ URL解析失败: {e}")

    # 4. 检查管理员用户
    print("\n4. 检查管理员用户:")
    try:
        admin_users = User.objects.filter(user_type='admin')
        print(f"   管理员用户数: {admin_users.count()}")
        for admin in admin_users:
            print(f"   - ID: {admin.id}, 用户名: {admin.username}, 超级用户: {admin.is_superuser}")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

    # 5. 如果有管理员用户，测试登录后的访问
    admin_user = User.objects.filter(user_type='admin').first()
    if admin_user:
        print(f"\n5. 测试管理员用户 '{admin_user.username}' 访问编辑页面:")
        try:
            # 强制登录
            client.force_login(admin_user)
            response = client.get('/courses/users/4/edit/')
            print(f"   状态码: {response.status_code}")
            if response.status_code == 200:
                print("   ✅ 管理员可以访问编辑页面")
                # 检查响应内容
                if 'form' in response.context:
                    print("   ✅ 表单在上下文中")
                else:
                    print("   ❌ 表单不在上下文中")
                if 'profile_form' in response.context:
                    print("   ✅ 档案表单在上下文中")
                else:
                    print("   ❌ 档案表单不在上下文中")
            elif response.status_code == 404:
                print("   ❌ 用户不存在或页面未找到")
            elif response.status_code == 403:
                print("   ❌ 权限不足")
            else:
                print(f"   ❌ 其他错误: {response.status_code}")
        except Exception as e:
            print(f"   ❌ 错误: {e}")
    else:
        print("\n5. ⚠️  没有找到管理员用户，无法测试登录后的访问")

    print("\n=== 测试完成 ===")

if __name__ == '__main__':
    test_user_edit_function()
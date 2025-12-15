#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from courses.views import AdminUserUpdateView

User = get_user_model()

print("=== 测试编辑视图 ===")

# 创建请求工厂
factory = RequestFactory()

try:
    # 创建模拟请求
    request = factory.get('/courses/users/4/edit/')

    # 获取用户
    user = User.objects.get(pk=4)
    print(f"测试用户: {user.username} ({user.user_type})")

    # 创建视图实例
    view = AdminUserUpdateView()
    view.request = request

    # 设置用户（模拟登录）
    admin_user = User.objects.filter(user_type='admin').first()
    if admin_user:
        view.request.user = admin_user
        print(f"使用管理员用户: {admin_user.username}")
    else:
        print("警告: 没有找到管理员用户")

    # 设置kwargs
    view.kwargs = {'pk': 4}

    # 测试获取对象
    obj = view.get_object()
    print(f"获取对象成功: {obj.username}")

    # 设置object属性
    view.object = obj

    # 测试获取表单
    form_class = view.get_form_class()
    print(f"表单类: {form_class}")

    # 测试获取上下文
    context = view.get_context_data()
    print(f"上下文 keys: {list(context.keys())}")

    print("视图测试成功")

except Exception as e:
    print(f"视图测试失败: {e}")
    import traceback
    traceback.print_exc()
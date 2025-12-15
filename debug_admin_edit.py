#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

print("=== 深度调试 AdminUserUpdateView ===")

from django.test import RequestFactory
from django.contrib.auth import get_user_model
from django.urls import reverse
from courses.views import AdminUserUpdateView

User = get_user_model()

# 1. 测试URL反向解析
print("\n1. 测试URL反向解析:")
try:
    url = reverse('courses:user_edit', kwargs={'pk': 4})
    print(f"   URL解析成功: {url}")
except Exception as e:
    print(f"   URL解析失败: {e}")

# 2. 获取用户
print("\n2. 获取测试用户:")
try:
    user = User.objects.get(pk=4)
    print(f"   用户4: {user.username} ({user.user_type})")
except User.DoesNotExist:
    print("   用户4不存在")
    exit()

# 3. 测试视图实例化
print("\n3. 测试视图实例化:")
try:
    view = AdminUserUpdateView()
    print("   视图实例化成功")

    # 检查视图属性
    print(f"   - model: {view.model}")
    print(f"   - form_class: {view.form_class}")
    print(f"   - template_name: {view.template_name}")
    print(f"   - context_object_name: {view.context_object_name}")
except Exception as e:
    print(f"   ❌ 视图实例化失败: {e}")

# 4. 模拟请求测试
print("\n4. 模拟请求测试:")
try:
    factory = RequestFactory()
    admin_user = User.objects.filter(user_type='admin').first()

    if not admin_user:
        print("   ❌ 没有找到管理员用户")
        exit()

    print(f"   使用管理员用户: {admin_user.username}")

    # 创建模拟请求
    request = factory.get('/courses/users/4/edit/')
    request.user = admin_user

    # 设置视图请求
    view.request = request
    view.kwargs = {'pk': 4}

    # 测试get_object
    obj = view.get_object()
    print(f"   ✅ get_object成功: {obj.username}")

    # 测试get_form_class
    form_class = view.get_form_class()
    print(f"   ✅ get_form_class成功: {form_class}")

    # 测试get_context_data
    view.object = obj
    context = view.get_context_data()
    print(f"   ✅ get_context_data成功，keys: {list(context.keys())}")

    # 检查关键上下文变量
    if 'form' in context:
        print("   ✅ form在上下文中")
    else:
        print("   ❌ form不在上下文中")

    if 'profile_form' in context:
        print("   ✅ profile_form在上下文中")
        if context['profile_form']:
            print(f"      - profile_form类型: {type(context['profile_form'])}")
    else:
        print("   ❌ profile_form不在上下文中")

    print("   ✅ 所有测试通过，视图应该正常工作")

except Exception as e:
    print(f"   ❌ 模拟请求测试失败: {e}")
    import traceback
    traceback.print_exc()

# 5. 测试路由解析
print("\n5. 测试路由解析:")
try:
    from django.urls import resolve
    resolved = resolve('/courses/users/4/edit/')
    print(f"   ✅ 路由解析成功:")
    print(f"      - view_name: {resolved.view_name}")
    print(f"      - func: {resolved.func}")
    print(f"      - kwargs: {resolved.kwargs}")
except Exception as e:
    print(f"   ❌ 路由解析失败: {e}")

print("\n=== 调试完成 ===")
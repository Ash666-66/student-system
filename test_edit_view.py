#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_system.settings')
django.setup()

from django.http import HttpResponse
from django.contrib.auth import get_user_model

def test_user_edit_view(request, pk):
    """临时测试视图"""
    User = get_user_model()
    try:
        user = User.objects.get(pk=pk)
        return HttpResponse(f"编辑视图工作正常！用户: {user.username} (ID: {pk})")
    except User.DoesNotExist:
        return HttpResponse(f"用户 {pk} 不存在", status=404)

print("测试视图函数已定义")
print("使用方法：在 courses/urls.py 中临时替换 AdminUserUpdateView 为这个视图函数")
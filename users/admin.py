from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, StudentProfile, TeacherProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('user_type', 'phone')}),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('扩展信息', {'fields': ('user_type', 'phone')}),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'gender', 'grade', 'major', 'class_name', 'user')
    list_filter = ('gender', 'grade', 'major', 'enrollment_date')
    search_fields = ('student_id', 'name', 'user__username', 'major')
    ordering = ('student_id',)


@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'name', 'gender', 'department', 'title', 'user')
    list_filter = ('gender', 'department', 'title', 'hire_date')
    search_fields = ('teacher_id', 'name', 'user__username', 'department')
    ordering = ('teacher_id',)
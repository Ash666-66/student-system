from django.contrib import admin
from .models import Course, CourseClass, Enrollment, Announcement


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'credits', 'hours', 'semester', 'academic_year', 'created_at')
    list_filter = ('semester', 'academic_year', 'credits', 'created_at')
    search_fields = ('course_code', 'course_name', 'description')
    ordering = ('-created_at',)


class CourseClassInline(admin.TabularInline):
    model = CourseClass
    extra = 0
    fields = ('class_code', 'teacher', 'classroom', 'schedule', 'max_students', 'current_students')
    readonly_fields = ('current_students',)


@admin.register(CourseClass)
class CourseClassAdmin(admin.ModelAdmin):
    list_display = ('class_code', 'course', 'teacher', 'classroom', 'schedule', 'current_students', 'max_students', 'created_at')
    list_filter = ('course__semester', 'course__academic_year', 'teacher', 'created_at')
    search_fields = ('class_code', 'course__course_name', 'course__course_code', 'teacher__username', 'classroom')
    ordering = ('-created_at',)
    readonly_fields = ('current_students', 'created_at', 'updated_at')


class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    extra = 0
    fields = ('student', 'status', 'enroll_time', 'approve_time', 'grade')
    readonly_fields = ('enroll_time', 'approve_time')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_class', 'status', 'enroll_time', 'approve_time', 'grade')
    list_filter = ('status', 'enroll_time', 'approve_time', 'course_class__course__semester')
    search_fields = ('student__username', 'course_class__course__course_name', 'course_class__class_code')
    ordering = ('-enroll_time',)
    readonly_fields = ('enroll_time', 'approve_time')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'course_class', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'author', 'course_class')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
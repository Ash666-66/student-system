from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # 仪表板
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 用户管理（管理员）- 放在前面避免与其他路由冲突
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/create/', views.admin_create_user_view, name='admin_create_user'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.user_edit_view, name='user_edit'),
    path('users/<int:pk>/delete/', views.admin_delete_user_view, name='admin_delete_user'),

    # 课程管理
    path('', views.CourseListView.as_view(), name='course_list'),
    path('<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('create/', views.CourseCreateView.as_view(), name='course_create'),
    path('<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # 课程班次管理
    path('classes/', views.CourseClassListView.as_view(), name='class_list'),
    path('classes/<int:pk>/', views.CourseClassDetailView.as_view(), name='class_detail'),
    path('classes/create/', views.CourseClassCreateView.as_view(), name='class_create'),
    path('classes/<int:pk>/update/', views.CourseClassUpdateView.as_view(), name='class_update'),
    path('classes/<int:pk>/delete/', views.CourseClassDeleteView.as_view(), name='class_delete'),
    path('classes/<int:class_id>/unenroll/', views.class_unenroll_view, name='class_unenroll'),

    # 选课管理
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enroll/<int:class_id>/', views.enroll_course_view, name='enroll_course'),
    path('enrollments/<int:enrollment_id>/approve/', views.approve_enrollment_view, name='approve_enrollment'),
    path('enrollments/<int:enrollment_id>/grade/', views.grade_enrollment_view, name='grade_enrollment'),
    path('enrollments/<int:enrollment_id>/cancel/', views.enrollment_cancel_view, name='enrollment_cancel'),

    # 公告管理
    path('announcements/create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
]
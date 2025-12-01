from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # 仪表板
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # 课程管理
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),

    # 课程班次管理
    path('classes/', views.CourseClassListView.as_view(), name='class_list'),
    path('classes/<int:pk>/', views.CourseClassDetailView.as_view(), name='class_detail'),
    path('classes/create/', views.CourseClassCreateView.as_view(), name='class_create'),
    path('classes/<int:pk>/update/', views.CourseClassUpdateView.as_view(), name='class_update'),

    # 选课管理
    path('enrollments/', views.EnrollmentListView.as_view(), name='enrollment_list'),
    path('enroll/<int:class_id>/', views.enroll_course_view, name='enroll_course'),
    path('enrollments/<int:enrollment_id>/approve/', views.approve_enrollment_view, name='approve_enrollment'),
    path('enrollments/<int:enrollment_id>/grade/', views.grade_enrollment_view, name='grade_enrollment'),

    # 用户管理（管理员）
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
]
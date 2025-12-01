from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('create_student_profile/<int:user_id>/', views.create_student_profile, name='create_student_profile'),
    path('create_teacher_profile/<int:user_id>/', views.create_teacher_profile, name='create_teacher_profile'),
]
from django.urls import path
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .views import RegisterView, LoginView, DashboardView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # URLs para redefinição de senha
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt'
    ), name='password_reset'),
    
    path('password_reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
] 
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, LoginView, DashboardView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # Outras URLs...
]
"""
URL configuration for finance_control project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import RegisterView, LoginView, LogoutView, DashboardView
from transactions.views import BalanceCreateView, TransactionListView
from budgets.views import BudgetListView, GoalListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('balance/create/', BalanceCreateView.as_view(), name='balance_create'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('budgets/', BudgetListView.as_view(), name='budget_list'),
    path('goals/', GoalListView.as_view(), name='goal_list'),
]

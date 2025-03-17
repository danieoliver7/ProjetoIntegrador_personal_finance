from django.urls import path
from . import views

urlpatterns = [
    path('balance/create/', views.BalanceCreateView.as_view(), name='balance_create'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
] 
from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('balance/create/', views.BalanceCreateView.as_view(), name='balance_create'),
    path('transactions/', views.TransactionListView.as_view(), name='transaction_list'),
    path('api/transactions/create/', api.create_transaction, name='api_transaction_create'),
] 
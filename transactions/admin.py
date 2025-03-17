from django.contrib import admin
from .models import Category, PaymentMethod, Transaction, Balance

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'user')
    list_filter = ('type', 'user')
    search_fields = ('name',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('user',)
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('description', 'amount', 'type', 'category', 'transaction_date', 'is_paid', 'user')
    list_filter = ('type', 'is_paid', 'category', 'transaction_date', 'user')
    search_fields = ('description',)
    date_hierarchy = 'transaction_date'
    list_editable = ('is_paid',)

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'date')
    list_filter = ('user', 'date')
    date_hierarchy = 'date'

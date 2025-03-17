from django.contrib import admin
from .models import Goal, Budget

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_amount', 'current_amount', 'progress_percentage', 'start_date', 'end_date', 'user')
    list_filter = ('user', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    date_hierarchy = 'end_date'
    readonly_fields = ('progress_percentage', 'is_completed')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'spent_amount', 'remaining_amount', 'progress_percentage', 'category', 'start_date', 'end_date', 'user')
    list_filter = ('user', 'category', 'start_date')
    search_fields = ('name',)
    date_hierarchy = 'start_date'
    readonly_fields = ('spent_amount', 'remaining_amount', 'progress_percentage')

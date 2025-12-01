from django.contrib import admin
from .models import HabitModel

class HabitAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'habit_type', 'category', 'reminder_time', 'duration_display', 'is_active', 'created_at', 'days_of_week', 'last_completed']
    list_filter = ['is_active', 'created_at', 'category', 'habit_type']
    search_fields = ['title', 'description', 'user__username']
    list_editable = ['is_active']

    def days_of_week_display(self, obj):
        """Красивое отображение дней недели"""
        if obj.days_of_week:
            days_dict = dict(HabitModel.DAYS_CHOICES)
            return ', '.join([days_dict.get(day, day) for day in obj.days_of_week])
        return "Не выбраны"
    days_of_week_display.short_description = 'Дни недели'

admin.site.register(HabitModel, HabitAdmin)
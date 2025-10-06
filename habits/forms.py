from django import forms
from .models import HabitModel


class HabitForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(
        choices=HabitModel.DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Дни недели',
        required=True
    )

    class Meta:
        model = HabitModel
        fields = ['title', 'description', 'habit_type', 'category', 'reminder_time', 'duration_minutes', 'days_of_week']
    
    def clean_days_of_week(self):
        """Проверка, что выбран хотя бы один день"""
        days = self.cleaned_data['days_of_week']
        if not days:
            raise forms.ValidationError('Выберите хотя бы один день недели')
        return days
    
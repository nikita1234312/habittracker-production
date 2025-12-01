import json
from django.db.models import Count
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from habits import models
from profiles.models import ProfileModel


def achievements_view(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    
    habits = request.user.habits.filter(is_active=True)
    total_habits = habits.count()
    
    habits_useful = models.HabitModel.objects.filter(user=request.user, habit_type='useful').count()
    habits_harmful = models.HabitModel.objects.filter(user=request.user, habit_type='harmful').count()

    weekly_data = get_weekly_completions(request.user)

    if request.user.is_authenticated:
        try:
            profile = ProfileModel.objects.get(user=request.user)
        except ProfileModel.DoesNotExist:
            pass
    
    context = {
        'profile': profile,
        'habits_data': json.dumps({
            'total_habits': total_habits,
            'weekly_data': weekly_data,
            'weekly_labels': ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
            'useful': habits_useful,
            'harmful': habits_harmful
        })
    }

    

    return render(request, 'achievements/achievements.html', context)


def get_weekly_completions(user):
    today = datetime.now().date()
    week_ago = today - timedelta(days=6)

    completions = models.HabitCompletionModel.objects.filter(habit__user=user, completed_at__range=[week_ago, today]).values('completed_at').annotate(count=Count('id'))

    weekly_data = [0] * 7

    for completion in completions:
        days_ago = (today - completion['completed_at']).days
        if days_ago >= 0 and days_ago <= 6:
            weekday = completion['completed_at'].weekday()
            weekly_data[weekday] += completion['count']

    return weekly_data
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required  
from django.http import JsonResponse
from .models import HabitModel
from profiles.models import ProfileModel
from .forms import HabitForm
from django.utils import timezone
from datetime import timedelta, date


@login_required
def habit_detail(request, habit_id):
    habit = get_object_or_404(HabitModel, id=habit_id, user=request.user)

    data = {
        'id': habit.id,
        'title': habit.title,
        'description': habit.description,
        'category': habit.category,
        'habit_type': habit.habit_type,
        'days_of_week': habit.days_of_week,
        'reminder_time': habit.reminder_time.strftime('%H:%M'),
        'duration_minutes': habit.duration_minutes,
        'is_completed_today': habit.is_completed_today
    }

    return JsonResponse(data)


@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()

            return JsonResponse({
                'status': 'success', 
                'message': 'Привычка успешно создана!',
                'habit_id': habit.id
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Исправьте ошибки в форме',
                'errors': form.errors.get_json_data()
            })
        
    return JsonResponse({
        'status': 'error', 
        'message': 'Метод не разрешен'
    }, status=405)

def get_category_icon(category_code):
    icons = {
        'learning': '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect width="8" height="18" x="3" y="3" rx="1"/>
            <path d="M7 3v18"/>
            <path d="M20.4 18.9c.2.5-.1 1.1-.6 1.3l-1.9.7c-.5.2-1.1-.1-1.3-.6L11.1 5.1c-.2-.5.1-1.1.6-1.3l1.9-.7c.5-.2 1.1.1 1.3.6Z"/>
        </svg>''',
        'sport': '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M10 14.66v1.626a2 2 0 0 1-.976 1.696A5 5 0 0 0 7 21.978"/>
            <path d="M14 14.66v1.626a2 2 0 0 0 .976 1.696A5 5 0 0 1 17 21.978"/>
            <path d="M18 9h1.5a1 1 0 0 0 0-5H18"/>
            <path d="M4 22h16"/>
            <path d="M6 9a6 6 0 0 0 12 0V3a1 1 0 0 0-1-1H7a1 1 0 0 0-1 1z"/>
            <path d="M6 9H4.5a1 1 0 0 1 0-5H6"/>
        </svg>''',
        'health': '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 9.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5"/>
        </svg>''',
        'relationships': '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/>
            <path d="M16 3.128a4 4 0 0 1 0 7.744"/>
            <path d="M22 21v-2a4 4 0 0 0-3-3.87"/>
            <circle cx="9" cy="7" r="4"/>
        </svg>''',
        'other': '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>
            <path d="m3.3 7 8.7 5 8.7-5"/>
            <path d="M12 22V12"/>
        </svg>'''
    }
    return icons.get(category_code, icons['other'])

def habits_list(request):
    if not request.user.is_authenticated:
        return redirect('signin')

    selected_category = request.GET.get('category', 'all')
    selected_status = request.GET.get('status', 'all')
    is_ajax = request.GET.get('ajax') == 'true'
    
    habits = HabitModel.objects.filter(user=request.user).order_by('-created_at')
    
    if selected_category != 'all':
        habits = habits.filter(category=selected_category)
    
    if selected_status != 'all':
        # if selected_status == 'active':
        #     habits = habits.filter(is_active=True)
        if selected_status == 'completed':
            time_24_hours_ago = timezone.now() - timedelta(hours=24)
            habits = habits.filter(last_completed=date.today())

    if is_ajax:
        habits_data = []
        for habit in habits:
            habits_data.append({
                'id': habit.id,
                'title': habit.title,
                'current_streak': habit.current_streak,
            })

        category_name = 'Все'
        if selected_category != 'all':
            category_name = dict(HabitModel.CATEGORY_CHOICES).get(selected_category, 'Все')

        return JsonResponse({
            'habits': habits_data,
            'category_name': category_name,
            'total_count': len(habits_data)
        })

    total_habits = habits.count()
    # active_habits = habits.filter(is_active=True).count()

    category_name = 'Все'
    if selected_category != 'all':
        category_name = dict(HabitModel.CATEGORY_CHOICES).get(selected_category, 'Все')

    try:
        profile = ProfileModel.objects.get(user=request.user)
    except ProfileModel.DoesNotExist:
        profile = None
        
    context = {
        'habits': habits,
        'total_habits': total_habits,
        # 'active_habits': active_habits,
        'current_category': selected_category, 
        'category_name': category_name,         
        'categories': HabitModel.CATEGORY_CHOICES,
        'profile': profile
        
    }
    return render(request, 'habits/habits.html', context)

@login_required
def complete_habit(request, habit_id):
    habit = get_object_or_404(HabitModel, id=habit_id, user=request.user)

    if habit.is_completed_today:
        pass
    else:
        habit.mark_completed()  

    return redirect('habits_list')

@login_required
def delete_habit(request, habit_id):
    habit = get_object_or_404(HabitModel, id=habit_id, user=request.user)
    habit.delete()

    return redirect('habits_list')
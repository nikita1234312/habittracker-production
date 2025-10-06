from django.shortcuts import render, redirect
from .models import HabitModel
from .forms import HabitForm

def habits_list(request):
    habits = HabitModel.objects.filter(user=request.user) 

    context = {
        'habits': habits
    }
    return render(request, 'habits/habits_list.html', context)

def add_habit(request):
    if  request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habits_list')
    else:
        form = HabitForm()
    return render(request, 'habits/habits_add.html', {'form': form})
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_habit, name='add_habit'),
    path('habits_list/', views.habits_list, name='habits_list'),
    path('<int:habit_id>/', views.habit_detail, name='habit_detail'),
]
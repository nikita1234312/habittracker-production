from django.urls import path
from .views import add_habit, habits_list

urlpatterns = [
    path('habits_add/', add_habit, name='habits_add'),
    path('habits_list/', habits_list, name='habits_list')
]
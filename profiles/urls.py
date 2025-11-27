from django.urls import path
from profiles import views

urlpatterns = [
    path('', views.profileView, name='profile'),
    path('edit/', views.profile_edit_view, name='profile_edit'),
]
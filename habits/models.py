from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import time


class HabitModel(models.Model):
    # Выборы
    HABIT_TYPE_CHOICES = [
        ('useful', 'Полезная'),
        ('harmful', 'Вредная')
    ]

    CATEGORY_CHOICES = [
        ('health', 'Здоровье'),
        ('sport', 'Спорт'),
        ('learning', 'Обучение'),
        ('productivity', 'Продуктивность'),
        ('finance', 'Финансы'),
        ('relationships', 'Отношения'),
        ('other', 'Другое'),
    ]

    DAYS_CHOICES = [
        ('mon', 'Понедельник'),
        ('tue', 'Вторник'),
        ('wed', 'Среда'),
        ('thu', 'Четверг'), 
        ('fri', 'Пятница'),
        ('sat', 'Суббота'),
        ('sun', 'Воскресенье'),
    ]
    # Дни, по которым нужно выполнить привычки
    days_of_week = models.JSONField(default=list, verbose_name='Дни недели')

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='habits',
        verbose_name='Пользователь'
    )

    title = models.CharField(max_length=80, verbose_name='Название')
    description = models.TextField(max_length=450, blank=True, verbose_name='Описание')
    
    habit_type = models.CharField(
        max_length=10,
        choices=HABIT_TYPE_CHOICES,
        verbose_name='Тип привычки'
    )

    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name='Категория'
    )

    # Время выполнения привычки (Во сколько)
    reminder_time = models.TimeField(
        default=time(9, 0),  
        verbose_name='Время выполнения',
    )

    # Длительность выполнения привычки
    duration_minutes = models.PositiveIntegerField(
        default=15,
        validators=[MinValueValidator(1), MaxValueValidator(240)], # Максимум до 4 часов
        verbose_name='Длительность (минуты)',
    )

    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    @property
    def duration_display(self):
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60


        def get_minutes_text(m):
            if m % 10 == 1 and m != 11:
                return "минута"
            elif m % 10 in [2, 3, 4] and m not in [12, 13, 14]:
                return "минуты"
            else:
                return "минут"


        if hours > 0 and minutes > 0:
            return f'{hours} {"часа" if hours in [2, 3, 4] else "час"} {minutes} {get_minutes_text(minutes)}'
        elif hours > 0:
            return f'{hours} {"часа" if hours in [2, 3, 4] else "час"}'
        else:
            return f'{minutes} {get_minutes_text(minutes)}'
        
    def __str__(self):
        return f"{self.title} ({self.get_habit_type_display()})"


    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['created_at']  # Сортировка по дате создания

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import time, date, datetime




class HabitModel(models.Model):
    # Выборы
    HABIT_TYPE_CHOICES = [
        ('useful', 'Полезная'),
        ('harmful', 'Вредная')
    ]

    CATEGORY_CHOICES = [
        ('health', 'Здоровье'),
        ('sport', 'Спорт'),
        ('learning', 'Образование'),
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
        validators=[MinValueValidator(1), MaxValueValidator(240)], # до 4 часов
        verbose_name='Длительность (минуты)',
    )

    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    current_streak = models.PositiveIntegerField(default=0, verbose_name='Текущая серия')
    best_streak = models.PositiveIntegerField(default=0, verbose_name='Лучшая серия')
    total_completions = models.PositiveIntegerField(default=0, verbose_name='Всего выполнений')
    total_time_minutes = models.PositiveIntegerField(default=0, verbose_name='Общее время (минуты)')
    success_rate = models.FloatField(default=0, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], verbose_name='Процент успеха')
    last_completed = models.DateField(null=True, blank=True, verbose_name='Последнее выполнение')

    def __str__(self):
        return f"{self.title} ({self.get_habit_type_display()})"
    
    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['created_at']

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
            
    @property
    def is_completed_today(self):
        """Проверяет, выполнена ли привычка сегодня"""
        if not self.last_completed:
            return False
        return self.last_completed == date.today()

    @property
    def days_since_creation(self):
        """Количество дней с момента создания привычки"""
        return (date.today() - self.created_at.date()).days

    @property
    def total_time_display(self):
        """Отображение общего времени в читаемом формате"""
        hours = self.total_time_minutes // 60
        minutes = self.total_time_minutes % 60
        
        if hours > 0 and minutes > 0:
            return f'{hours}ч {minutes}м'
        elif hours > 0:
            return f'{hours}ч'
        else:
            return f'{minutes}м'
        
    @property
    def get_active_days_display(self):
        """Отображение активных дней в читаемом формате"""
        day_names = {
            'mon': 'Пн', 'tue': 'Вт', 'wed': 'Ср', 
            'thu': 'Чт', 'fri': 'Пт', 'sat': 'Сб', 'sun': 'Вс'
        }

        return [day_names[day] for day in self.days_of_week]

    def mark_completed(self):
        """Отметить привычку как выполненную на сегодня"""
        today = date.today()
        if self.last_completed == today:
            return False
        
        HabitCompletionModel.objects.get_or_create(habit=self, completed_at=today)

        self.total_completions += 1
        self.total_time_minutes += self.duration_minutes
        if self.last_completed and (today - self.last_completed).days == 1:
            self.current_streak += 1
        else:
            self.current_streak = 1
        if self.current_streak > self.best_streak:
            self.best_streak = self.current_streak
            
        self.last_completed = today
        days_active = self.days_since_creation
        if days_active > 0:
            self.success_rate = (self.total_completions / days_active) * 100
        else:
            self.success_rate = 100.0  
        
        self.save()
        return True

    def reset_streak(self):
        """Сбросить текущую серию (при пропуске)"""
        self.current_streak = 0
        self.save()

    def get_stats_for_display(self):
        """Получить статистику для отображения в модальном окне"""
        return {
            'current_streak': self.current_streak,
            'best_streak': self.best_streak,
            'total_completions': self.total_completions,
            'total_time': self.total_time_display,
            'success_rate': round(self.success_rate, 1),
            'is_completed_today': self.is_completed_today,
        }


class HabitCompletionModel(models.Model):
    habit = models.ForeignKey(HabitModel, on_delete=models.CASCADE)
    completed_at = models.DateField(default=date.today, verbose_name='Дата выполнения')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Выполнение привычки'
        verbose_name_plural = 'Выполнения привычек'
        unique_together = ['habit', 'completed_at']
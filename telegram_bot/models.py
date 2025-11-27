from django.db import models
from django.contrib.auth.models import User

class TgUser(models.Model):
    chat_id = models.BigIntegerField(unique=True, verbose_name="ID чата")
    django_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='telegram_user', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    temp_username = models.CharField(max_length=150, blank=True, null=True)
    auth_step = models.CharField(max_length=20, default='idle')


    auth_step = models.CharField(
        max_length=20, 
        default='idle', 
        choices=[
            ('idle', 'Ожидание'),
            ('waiting_username', 'Ожидает логин'),
            ('waiting_password', 'Ожидает пароль')
        ]
    )
    
    def __str__(self):
        if self.django_user:
            return f"ТГ: {self.chat_id} - Пользователь: {self.django_user.username}"
        return f"TГ: {self.chat_id} - Не подключено"
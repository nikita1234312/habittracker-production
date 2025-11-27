from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from habits.models import HabitModel
from telegram_bot.models import TgUser
import requests
import time
import random
from datetime import datetime

MOTIVATIONAL_PHRASES = [
    "Ты сможешь! Всего пару минут и дело сделано!",
    "Маленький шаг каждый день - большой результат через год!",
    "Пора действовать! Ты будешь гордиться собой после!",
    "Не откладывай на завтра то, что можно сделать сейчас!",
    "Каждая выполненная привычка - это победа над собой!",
    "Ты становишься лучше с каждой выполненной задачей!",
    "Вперед к цели! Ты уже на полпути к успеху!",
    "Сильные люди создают привычки, слабые - оправдания!",
    "Сделай это сейчас и освободи вечер для отдыха!",
    "Твое будущее я скажет тебе спасибо!",
    "Небольшое усилие сейчас - огромные перемены потом!",
    "Ты сильнее, чем думаешь! Просто начни!",
    "Каждый раз, когда ты выполняешь привычку, ты становишься на 1% лучше!",
    "Не сдавайся! Ты уже так близок к цели!",
    "Помни: дисциплина = свобода! Сделай и будь свободен!"
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Запуск автоматической проверки напоминаний...')
        
        if not hasattr(settings, 'BOT_TOKEN') or not settings.BOT_TOKEN:
            self.stdout.write('BOT_TOKEN не найден в settings.py')
            return

        try:
            while True:
                self.check_reminders()
                time.sleep(60)
                
        except KeyboardInterrupt:
            self.stdout.write('Остановка автоматической проверки...')
        except Exception as e:
            self.stdout.write(f'Ошибка в основном цикле: {e}')

    def check_reminders(self):
        now = datetime.now()
        current_time = now.time()
        current_minute = now.minute
        current_hour = now.hour

        self.stdout.write(f'[{datetime.now().strftime("%H:%M:%S")}] Проверка напоминаний...')
        self.stdout.write(f'Текущее время: {current_hour:02d}:{current_minute:02d}')

        try:
            all_habits = HabitModel.objects.all()
            self.stdout.write(f'Всего привычек в базе: {all_habits.count()}')
            
            for habit in all_habits:
                self.stdout.write(f'Привычка: "{habit.title}" - время: {habit.reminder_time} - пользователь: {habit.user.username}')

            active_habits = HabitModel.objects.filter(
                reminder_time__hour=current_hour,
                reminder_time__minute=current_minute
            )

            self.stdout.write(f'Найдено привычек для напоминания: {active_habits.count()}')

            for habit in active_habits:
                self.stdout.write(f'Отправляем напоминание: "{habit.title}" для {habit.user.username}')
                self.send_reminder(habit)

        except Exception as e:
            self.stdout.write(f'Ошибка при проверке привычек: {e}')

    def send_reminder(self, habit):
        try:
            try:
                tg_user = TgUser.objects.get(django_user=habit.user)
                chat_id = tg_user.chat_id
            except TgUser.DoesNotExist: 
                self.stdout.write(f'Пользователя - {habit.user} - нет в телеграмм')
                return False
            
            motivation = random.choice(MOTIVATIONAL_PHRASES)

            msg = f'<b>Пора выполнить привычку!</b>\n\n{habit.title} \nОписание: {habit.description} \n\n{motivation}'

            url = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage'

            data = {
                'chat_id': chat_id,
                'text': msg,
                'parse_mode': 'HTML'            
            }

            response = requests.post(url, json=data)

            if response.status_code == 200:
                self.stdout.write(f'Напоминание {habit.title} для {habit.user.username} успешно отправлено!')
                return True
            else:
                self.stdout.write(f'Напоминание {habit.title} для {habit.user.username} не отправлено, статус ошибки - {response.status_code}')
                return False
        except Exception as e:
            self.stdout.write(f'Ошибка при отправке {habit.title} - {e}')
            return False
from django.core.management.base import BaseCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram_bot import views
from django.conf import settings

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Запуск бота...')

        if not hasattr(settings, 'BOT_TOKEN') or not settings.BOT_TOKEN:
            self.stdout.write('BOT_TOKEN не найден в settings.py')
            return

        try:
            application = Application.builder().token(settings.BOT_TOKEN).build()
            
            application.add_handler(CommandHandler("start", views.start_command))
            application.add_handler(CommandHandler("link", views.link_command))
            application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, views.handle_message))
            
            self.stdout.write('Бот запущен! Ожидаем сообщения...')

            application.run_polling()
            
        except Exception as e:
            self.stdout.write(f'Ошибка запуска бота: {e}')
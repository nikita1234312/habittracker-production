from telegram import Update
from telegram.ext import ContextTypes
from django.contrib.auth import authenticate
from .models import TgUser
from asgiref.sync import sync_to_async

@sync_to_async
def get_or_create_tg_user(chat_id):
    return TgUser.objects.get_or_create(chat_id=chat_id)

@sync_to_async  
def get_tg_user(chat_id):
    try:
        return TgUser.objects.get(chat_id=chat_id)
    except TgUser.DoesNotExist:
        return None

@sync_to_async
def authenticate_user(username, password):
    return authenticate(username=username, password=password)

@sync_to_async
def update_tg_user_auth_step(chat_id, auth_step, username=None):
    tg_user = TgUser.objects.get(chat_id=chat_id)
    tg_user.auth_step = auth_step
    if username:
        tg_user.temp_username = username
    tg_user.save()
    return tg_user

@sync_to_async
def complete_linking(chat_id, user):
    tg_user = TgUser.objects.get(chat_id=chat_id)
    tg_user.django_user = user
    tg_user.temp_username = None
    tg_user.auth_step = 'idle'
    tg_user.save()
    return tg_user

@sync_to_async
def reset_auth_step(chat_id):
    tg_user = TgUser.objects.get(chat_id=chat_id)
    tg_user.auth_step = 'idle'
    tg_user.temp_username = None
    tg_user.save()
    return tg_user

@sync_to_async
def check_user_linked(chat_id):
    try:
        tg_user = TgUser.objects.get(chat_id=chat_id)
        return tg_user.django_user is not None
    except TgUser.DoesNotExist:
        return False

@sync_to_async
def get_tg_user_with_username(chat_id):
    try:
        tg_user = TgUser.objects.select_related('django_user').get(chat_id=chat_id)
        if tg_user.django_user:
            return tg_user.django_user.username
        return None
    except TgUser.DoesNotExist:
        return None

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await get_or_create_tg_user(chat_id)

    photo_url = 'https://i.pinimg.com/originals/05/3a/08/053a0826a8c0c0011b954494bafed505.jpg'

    await update.message.reply_photo(
        photo=photo_url,
        caption='Привет! Я бот помощник для трекера привычек HabitTracker. Я буду напоминать тебе о твоих привычках!\n\nДля начала нужно привязать аккаунт с помощью команды /link'
    )

async def link_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    is_linked = await check_user_linked(chat_id)
    if not is_linked:
        await update_tg_user_auth_step(chat_id, 'waiting_username')
        await update.message.reply_text('Введите ваш логин от сайта:')
    else:
        username = await get_tg_user_with_username(chat_id)
        if username:
            await update.message.reply_text(f'Аккаунт уже привязан: {username}')
        else:
            await update.message.reply_text('Аккаунт уже привязан')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    if text.startswith('/'):
        return
    
    tg_user = await get_tg_user(chat_id)
    if not tg_user:
        await update.message.reply_text("Сначала используйте /start")
        return
    
    if tg_user.auth_step == 'waiting_username':
        await update_tg_user_auth_step(chat_id, 'waiting_password', username=text)
        await update.message.reply_text("Введите ваш пароль:")
        
    elif tg_user.auth_step == 'waiting_password':
        username = tg_user.temp_username
        user = await authenticate_user(username, text)

        if user is not None:
            await complete_linking(chat_id, user)
            await update.message.reply_text(f'Аккаунт {username} успешно привязан!')
        else:
            await reset_auth_step(chat_id)
            await update.message.reply_text(f'Неверный логин или пароль! Используйте /link для повторной попытки')
    
    else:
        await update.message.reply_text("Используйте /link для привязки аккаунта")
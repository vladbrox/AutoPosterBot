from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import time
from message import message_text

# Настройки
TOKEN = "your token"  # Замените на токен вашего бота от @BotFather
CHANNEL_ID = "@feed"  # Замените на ID вашего канала (например, @feed)

#Замените на подходящий текст
WELCOME_MESSAGE = (
        "Привет! Я бот, созданный по инструкции github.com/vladbrox/JustPostBot.\n"
        "Используй /debug, чтобы проверить сообщение."
)
ERROR_MESSAGE = "Эта команда доступна только администраторам канала."

#Настройте нужное время
HOUR=6
MINUTE=0
SECOND=0

# Ежедневная отправка сообщения в канал
async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    message = message_text
    await context.bot.send_message(chat_id=CHANNEL_ID, text=message)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_user.id, text=WELCOME_MESSAGE)

# Проверка, является ли пользователь администратором канала
async def is_channel_admin(bot, user_id, channel_id):
    try:
        admins = await bot.get_chat_administrators(channel_id)
        return any(admin.user.id == user_id for admin in admins)
    except Exception as e:
        print(f"Ошибка проверки статуса администратора: {e}")
        return False

# Обработчик команды /debug с проверкой администратора
async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_channel_admin(context.bot, user_id, CHANNEL_ID):
        usd_byn, btc_byn, ton_byn = get_exchange_rates()
        message = format_message(usd_byn, btc_byn, ton_byn)
        await context.bot.send_message(chat_id=user_id, text=message)
    else:
        await context.bot.send_message(chat_id=user_id, text=ERROR_MESSAGE)

# Основная функция запуска бота
def main():
    # Создание приложения
    application = Application.builder().token(TOKEN).build()

    # Добавление обработчиков команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("debug", debug))

    # Настройка ежедневной задачи (9:00 МСК = 6:00 UTC)
    job_queue = application.job_queue
    if job_queue is None:
        raise RuntimeError("JobQueue не доступен. Установите python-telegram-bot[job-queue].")
    job_queue.run_daily(send_daily_message, time(hour=HOUR, minute=MINUTE, second=SECOND))

    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

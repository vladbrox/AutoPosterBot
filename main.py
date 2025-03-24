import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import time

# Настройки
TOKEN = "your token"  # Замените на токен вашего бота от @BotFather
CHANNEL_ID = "@feed"  # Замените на ID вашего канала (например, @feed)

#Замените на подходящий текст
WELCOME_MESSAGE = (
        "Привет! Я бот, который ежедневно отправляет курсы валют в канал.\n"
        "Используй /debug, чтобы проверить текущие курсы (доступно только администраторам канала)."
)
ERROR_MESSAGE = "Эта команда доступна только администраторам канала."

#Настройте нужное время
HOUR=6
MINUTE=0
SECOND=0

# API-эндпоинты
CURRENCYFREAKS_URL = "https://api.currencyfreaks.com/v2.0/rates/latest?apikey=YOUR_API_KEY" #Замените apikey= на свой API ключ с сайта currencyfreaks.com
COINGECKO_BTC_URL = "https://api.coingecko.com/api/v3/coins/bitcoin"
COINGECKO_TON_URL = "https://api.coingecko.com/api/v3/coins/the-open-network"

# Функция получения курсов валют
def get_exchange_rates():
    try:
        # Получение курса USD/BYN
        response = requests.get(CURRENCYFREAKS_URL)
        response.raise_for_status()
        usd_byn = float(response.json()["rates"]["BYN"])
    except Exception as e:
        print(f"Ошибка CurrencyFreaks: {e}")
        usd_byn = "N/A"

    try:
        # Получение курса BTC в USD
        response = requests.get(COINGECKO_BTC_URL)
        response.raise_for_status()
        btc_usd = float(response.json()["market_data"]["current_price"]["usd"])
    except Exception as e:
        print(f"Ошибка CoinGecko (BTC): {e}")
        btc_usd = "N/A"

    try:
        # Получение курса TON в USD
        response = requests.get(COINGECKO_TON_URL)
        response.raise_for_status()
        ton_usd = float(response.json()["market_data"]["current_price"]["usd"])
    except Exception as e:
        print(f"Ошибка CoinGecko (TON): {e}")
        ton_usd = "N/A"

    # Конвертация в BYN
    if usd_byn != "N/A" and btc_usd != "N/A":
        btc_byn = round(btc_usd * usd_byn)  # Округляем до целого числа
    else:
        btc_byn = "N/A"

    if usd_byn != "N/A" and ton_usd != "N/A":
        ton_byn = round(ton_usd * usd_byn, 2)
    else:
        ton_byn = "N/A"

    return round(usd_byn, 2) if usd_byn != "N/A" else "N/A", btc_byn, ton_byn

# Форматирование сообщения с запятыми как разделителями тысяч
def format_message(usd_byn, btc_byn, ton_byn):
    usd_str = f"{usd_byn:,.2f}" if usd_byn != "N/A" else "N/A"
    btc_str = f"{btc_byn:,}" if btc_byn != "N/A" else "N/A"
    ton_str = f"{ton_byn:,.2f}" if ton_byn != "N/A" else "N/A"

    return (
        "Курс валют на сегодня!\n"
        f"• usd - {usd_str} BYN\n"
        f"• btc - {btc_str} BYN\n"
        f"• ton - {ton_str} BYN"
    )

# Ежедневная отправка сообщения в канал
async def send_daily_message(context: ContextTypes.DEFAULT_TYPE):
    usd_byn, btc_byn, ton_byn = get_exchange_rates()
    message = format_message(usd_byn, btc_byn, ton_byn)
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

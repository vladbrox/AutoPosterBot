#Это приведино как пример. Вы можете все удалить и написать свою функцию message_text, которая возвращает string переменную с нужным вам текстом
#Этот пример отправляет курсы валют

import requests

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

#Функция отправки, она должна обязательно присутсвовать
def message_text():
    usd_byn, btc_byn, ton_byn = get_exchange_rates()
    message = format_message(usd_byn, btc_byn, ton_byn)
    return message
# AutoPosterBot

Этот бот позволяет автоматически публиковать сообщения в вашем Telegram-канале. Настройте его один раз, и он будет работать без вашего участия!

## Возможности

* Автоматическая публикация сообщений по расписанию.
* Легкая настройка и развертывание.
* Возможность настройки контента сообщений.
* Бесплатный хостинг (с ограничениями).

## Начало работы

### 1. Настройка Telegram

1.  Создайте нового Telegram-бота с помощью [@BotFather](https://t.me/botfather).
2.  Получите API-ключ (токен) вашего бота.
3.  Добавьте бота в ваш Telegram-канал в качестве администратора с правами на публикацию сообщений.

### 2. Подготовка к запуску

1.  Установите Python 3.9 или более позднюю версию с [python.org](https://www.python.org/).
2.  Клонируйте этот репозиторий на свой компьютер.
3.  Установите необходимые библиотеки, указанные в файле `requirements.txt`, с помощью команды:

    ```bash
    pip install -r requirements.txt
    ```

4.  Откройте файл `main.py` и замените следующие константы на свои значения:

    * `TOKEN`: API-ключ вашего Telegram-бота.
    * `CHANNEL_ID`: ID вашего Telegram-канала (например @snow).
5.  Функция `send_daily_message()` отвечает за формирование контента сообщения. Измените ее, чтобы бот публиковал нужную вам информацию.

### 3. Запуск бота

Запустите бота, выполнив команду:

```bash
python main.py
```

Бот начнет работать и публиковать сообщения в соответствии с настройками.

### Развертывание на хостинге
Для постоянной работы бота рекомендуется использовать облачный хостинг.
Railway.com (рекомендуется)
 * Зарегистрируйтесь на [railway.com](https://railway.com/) через GitHub.
 * Авторизуйте доступ Railway к вашему репозиторию.
 * Создайте новый проект и выберите ваш репозиторий.
 * Railway автоматически развернет вашего бота и установит все библиотеки.
> [!TIP]
> Railway предоставляет бесплатный пробный период с кредитом в $5. Ежедневное потребление ресурсов составляет около ¢1. Таким образом, бесплатного периода хватит примерно на 500 дней непрерывной работы.

### Вклад
Приветствуются любые улучшения и дополнения к этому проекту. Если у вас есть идеи или предложения, создайте issue или отправьте pull request.

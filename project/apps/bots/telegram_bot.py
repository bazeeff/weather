from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests


import environ

env = environ.Env()

TELEGRAM_API_TOKEN = env('TELEGRAM_API_TOKEN')

API_URL = 'http://web:8000/api/v1/weather/search_address/'
API_TIMEOUT = 100


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Привет! Отправь мне название города, и я пришлю прогноз погоды.")


async def get_weather(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    city_name = update.message.text.strip()
    city_name = city_name.capitalize()
    await update.message.reply_text(f"Ищу прогноз погоды для города {city_name}...")

    # Запрос к DRF API для получения прогноза погоды
    try:
        response = requests.get(API_URL, params={'query': city_name}, timeout=API_TIMEOUT)
        response.raise_for_status()
        weather_data = response.json()

        # Формирование сообщения о погоде
        weather_message = (
            f"Погода в городе {weather_data['city']}:\n"
            f"Температура: {weather_data['temperature']}°C\n"
            f"Давление: {weather_data['pressure']} мм рт. ст.\n"
            f"Скорость ветра: {weather_data['wind_speed']} м/с"
        )
    except requests.RequestException:
        weather_message = "Не удалось получить данные о погоде. Пожалуйста, попробуйте позже."

    # Отправка ответа пользователю
    await update.message.reply_text(weather_message)


def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_weather))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()

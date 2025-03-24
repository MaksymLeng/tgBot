import telebot
import schedule
import time
import threading
import os

TOKEN = os.environ.get('TELEGRAM_TOKEN')
USER_ID = int(os.environ.get('TELEGRAM_USER_ID'))

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Бот для напоминаний запущен! Я буду тебя будить и следить за парами.")

# Функция для отправки сообщений

def send_reminder(message):
    bot.send_message(USER_ID, message)

# Расписание уведомлений

def schedule_jobs():
    schedule.every().day.at("10:00").do(send_reminder, message="Подъём! Вставай и начинай день!")
    schedule.every().monday.at("06:30").do(send_reminder, message="Понедельник! В 7:30 физика — пора собираться!")
    schedule.every().wednesday.at("07:15").do(send_reminder, message="Среда! В 8:15 онлайн пара — подключайся!")

# Поток для работы планировщика

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_jobs()
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()
    bot.polling(none_stop=True)

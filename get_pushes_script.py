import asyncio
import os

from telebot import TeleBot
import firebase_admin
from firebase_admin import firestore, credentials

from dotenv import load_dotenv, find_dotenv
import tracemalloc
tracemalloc.start()

load_dotenv(find_dotenv())

# Настройки бота и Firebase
bot = TeleBot(os.getenv('SEND_BOT_TOKEN'))
cred = credentials.Certificate(os.getenv('FIREBASE_CONFIG_PATH'))
firebase_admin.initialize_app(cred, {'databaseURL': os.getenv('DATABASE_URL')})
db = firestore.client()

admin = os.getenv('ADMIN_ID')


def on_snapshot(col_snapshot, changes, read_time):
    for change in changes:
        if change.type.name == 'ADDED':
            # Получить данные новой записи
            new_record_data = change.document.to_dict()

            # Отправить сообщение в Telegram-чат
            bot.send_message(admin, 'Новая запись добавлена в базу данных:\n' + str(new_record_data))


# Подписаться на обновления в коллекции "records"
db.collection('records').on_snapshot(on_snapshot)


async def main():
    # Запуск бота
    await bot.infinity_polling()


if __name__ == '__main__':
    asyncio.run(main())

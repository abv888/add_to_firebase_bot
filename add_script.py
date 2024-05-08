import asyncio
import os

from telebot.async_telebot import AsyncTeleBot
from telebot import types
import firebase_admin
from firebase_admin import firestore, credentials

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Настройки бота и Firebase
bot = AsyncTeleBot(os.getenv('ADD_BOT_TOKEN'))
cred = credentials.Certificate(os.getenv('FIREBASE_CONFIG_PATH'))
firebase_admin.initialize_app(cred, {'databaseURL': os.getenv('DATABASE_URL')})
db = firestore.client()


def check_value(message, val):
    # Получить значение для проверки # Удалить команду 'Проверить значение'

    # Получить все документы из коллекции
    docs = db.collection('records').stream()  # Замените 'records' на фактическое название коллекции

    # Флаг для отслеживания, было ли найдено значение
    value_found = False

    for doc in docs:
        # Проверить наличие значения в документе
        if val in doc.to_dict().values():
            value_found = True
            break

    return value_found
    # Отправить сообщение в зависимости от результата проверки
    # if value_found:
    #     await bot.send_message(message.chat.id, 'Значение найдено в базе данных!')
    # else:
    #     await bot.send_message(message.chat.id, 'Значение не найдено в базе данных.')


async def add_element(message):
    # Получить данные элемента из сообщения
    element_data = int(message.text)  # Удалить команду 'Добавить элемент'

    if not check_value(message, element_data):

    # Добавить элемент в базу данных
        db.collection('records').add({f"{element_data}": element_data})

    # Отправить сообщение пользователю о добавлении
        await bot.send_message(message.chat.id, 'Элемент успешно добавлен в базу данных!')
    else:
        await bot.send_message(message.chat.id, 'Элемент уже есть в базе данных!')


async def main():
    # Обработчик команды добавления элемента
    bot.register_message_handler(add_element)

    # Запуск бота
    await bot.polling()


if __name__ == '__main__':
    asyncio.run(main())

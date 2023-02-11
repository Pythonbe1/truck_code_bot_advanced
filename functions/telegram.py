from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from functions import bot_functions as b
from functions import markup as nav
import os


def telegram_bot(token_data):
    # nest_asyncio.apply()
    bot = Bot(token_data)
    dp = Dispatcher(bot)
    conversation_state = {}

    @dp.message_handler(commands='start')
    async def start_message(message: types.Message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        surname = message.from_user.last_name
        username = message.from_user.username
        await bot.send_message(message.from_user.id, 'Хотите добавить трек-код? Нажмите кнопку ДОБАВИТЬ ТРЕК-КОДЫ',
                               reply_markup=nav.keyboard1)
        sql = f"SELECT * from user_info where user_id={user_id}"
        a = len(b.get_data_from_db(sql))
        if a == 0:
            b.insert_db(user_id, first_name, surname, username, 'insert')

    @dp.callback_query_handler(lambda c: c.data == 'button1')
    async def process_callback_start_messages(callback_query: CallbackQuery):
        await bot.send_message(chat_id=callback_query.message.chat.id, text="Добавьте Ваши трек-коды друг за другом и потом нажимите"
                                                                " кнопку ЗАКОНЧИТЬ")
        conversation_state[callback_query.message.chat.id] = 'waiting_for_message'

    @dp.message_handler(lambda message: conversation_state.get(message.chat.id) == 'waiting_for_message')
    async def process_message(message: types.Message):
        state = conversation_state.get(message.chat.id)
        if state == 'waiting_for_message':
            b.insert_chat_id__truck_number(message.chat.id, message.text, 'insert')
            await bot.send_message(chat_id=message.chat.id, text='Ваш трек-код добавлен в базу: ' + message.text)
    executor.start_polling(dp, skip_updates=True)

from functions import markup as nav
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold
from aiogram.dispatcher.filters import Text
import nest_asyncio
from functions import bot_functions as b


def telegram_bot(token_data):
    nest_asyncio.apply()
    bot = Bot(token_data, parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot)

    @dp.message_handler(commands='start')
    async def start_message(message: types.Message):
        user_id = message.from_user.id
        first_name = message.from_user.first_name
        surname = message.from_user.last_name
        username = message.from_user.username
        await bot.send_message(message.from_user.id, 'Хотите добавить трек-код? Нажите кнопку ДОБАВИТЬ ТРЕК-КОДЫ')
        await bot.send_message(message.from_user.id, 'Уже добавили? Нажите кнопку ДОБАВЛЕНЫ ТРЕК-КОДЫ')
        await bot.send_message(message.from_user.id, 'Выберите ...', reply_markup=nav.mainMenu)
        a = len(b.get_data_from_db(user_id))
        if a == 0:
            b.insert_db(user_id, first_name, surname, username, 'insert')






    @dp.message_handler(Text(equals='ДОБАВИТЬ ТРЕК-КОД'))
    async def add(message: types.Message):
        await bot.send_message(message.from_user.id, 'Добавьте Ваши трек-коды друг за другом ')

    @dp.message_handler(Text(equals='ДОБАВЛЕНЫ ТРЕК-КОДЫ'))
    async def added(message: types.Message):
        print('Nurgul')

    executor.start_polling(dp, skip_updates=True)

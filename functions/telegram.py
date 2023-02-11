from datetime import date

import nest_asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold
from functions import bot_functions as b
from functions import markup as nav
from functions.bot_functions import get_data_from_db
import requests


def telegram_bot_sendtext(token, bot_message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chat_id = 309032069
    data = {
        "chat_id": chat_id,
        "text": bot_message
    }
    response = requests.post(url, json=data)



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
        await bot.send_message(message.from_user.id, 'Хотите добавить трек-код? Нажмите кнопку *ДОБАВИТЬ ТРЕК-КОД*'
                                                     '\n Хотите посмотреть список добавленных трек-кодов? Нажмите кнопку *ДОБАВЛЕННЫЕ ТРЕК-КОДЫ*',
                               parse_mode=types.ParseMode.MARKDOWN,
                               reply_markup=nav.mainMenu)
        sql = f"SELECT * from user_info where user_id={user_id}"
        a = len(b.get_data_from_db(sql))
        if a == 0:
            b.insert_db(user_id, first_name, surname, username, 'insert')

    @dp.message_handler(Text(equals='ДОБАВИТЬ ТРЕК-КОД'))
    async def add_truck_code(message: types.Message):
        await bot.send_message(message.from_user.id, 'После добавление трек-кодов нажмите кнопку *ЗАВЕРШИТЬ*',
                               reply_markup=nav.finishMenu, parse_mode=types.ParseMode.MARKDOWN, )

        @dp.message_handler()
        async def adding_truck_codes(message_2: types.Message):
            chat_id = message_2.from_user.id
            truck_code = message_2.text
            today = date.today()
            b.insert_chat_id__truck_number(chat_id, truck_code, today, kind='insert')
            await bot.send_message(message_2.from_user.id, f'Трек-код добавлен: *{truck_code}*'
                                                           f'\nПосле добавление трек-кодов нажмите кнопку *ЗАВЕРШИТЬ*',
                                   reply_markup=nav.finishMenu, parse_mode=types.ParseMode.MARKDOWN)

    @dp.message_handler(Text(equals='ЗАВЕРШИТЬ'))
    async def finish(message: types.Message):
        chat_id = message.from_user.id
        first_name = message.from_user.first_name
        surname = message.from_user.last_name
        username = message.from_user.username

        sql = f"""select * from user_truck_info where chat_id={chat_id} and is_paid=False"""
        data = get_data_from_db(sql)
        bot_message = f'chat_id: {chat_id}' \
                      f'\nfirstname: {first_name}' \
                      f'\nlastname: {surname}' \
                      f'\nusername: {username}' \
                      f'\nдобавил количество трек-кодов: {len(data)}' \
                      f'\nдолжен скинуть чек на сумму: {len(data) * 30} тенге'
        print(bot_message)
        telegram_bot_sendtext(token_data, bot_message)
        await bot.send_message(message.from_user.id,
                               f"Количество добавленных и не оплаченных трек-кодов: {hbold(len(data))}"
                               f"\nЧтобы получать уведомление прошу оплатить: {hbold(len(data) * 30)} тенге"
                               f"\nОбращайтесь к Нургуль Абенова https://t.me/AbenovaNT '")



    @dp.message_handler(Text(equals='ДОБАВЛЕННЫЕ ТРЕК-КОДЫ'))
    async def check_truck_code(message: types.Message):
        chat_id = message.from_user.id
        sql = f"""select t.truck_code, t.added_date from user_truck_info t where t.chat_id={chat_id}"""
        data = get_data_from_db(sql)
        data['added_date'] = data['added_date'].astype(str)
        date_list = list(data['added_date'].unique())
        if len(date_list) != 0:
            result = []
            for date in date_list:
                result.append({
                    'Дата': date,
                    'Трек коды': list(data[data.added_date.isin([date])]['truck_code'])
                })
            for index, item in enumerate(result):
                await message.answer(f"{hbold('Дата: ')}{item.get('Дата')}\n"
                                     f"{hbold('Трек-код: ')}{item.get('Трек коды')}")
        else:
            await message.answer(f"{hbold('У вас нет трек-кодов')}")

    executor.start_polling(dp, skip_updates=True)

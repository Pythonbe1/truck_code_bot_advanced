import asyncio
import os
from datetime import date
import nest_asyncio
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold
from functions import insert_update_db as b
from functions import markup as nav
from functions.insert_update_db import get_data_from_db
import requests
from dotenv import load_dotenv
import schedule

load_dotenv()


def telegram_bot_sendtext(token, bot_message, chat_id):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    chat_id = chat_id
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

        if int(user_id) not in [309032069]:
            await bot.send_message(message.from_user.id, 'Хотите добавить трек-код? Нажмите кнопку *ДОБАВИТЬ ТРЕК-КОД*'
                                                         '\n Хотите посмотреть список добавленных трек-кодов? Нажмите кнопку *ДОБАВЛЕННЫЕ ТРЕК-КОДЫ*',
                                   parse_mode=types.ParseMode.MARKDOWN,
                                   reply_markup=nav.mainMenu)
        else:
            await bot.send_message(message.from_user.id, 'Хотите добавить трек-код? Нажмите кнопку *ДОБАВИТЬ ТРЕК-КОД*'
                                                         '\n Хотите посмотреть список добавленных трек-кодов? Нажмите кнопку *ДОБАВЛЕННЫЕ ТРЕК-КОДЫ*'
                                                         '\n Хотите открыть доступ на chat_id? Нажмите кнопку *ОТКРЫТЬ ДОСТУП В CHAT_ID*',
                                   parse_mode=types.ParseMode.MARKDOWN,
                                   reply_markup=nav.nurgul_button)

        sql = f"SELECT * from user_info where chat_id={user_id}"
        a = len(b.get_data_from_db(sql))
        if a == 0:
            b.insert_db(user_id, first_name, surname, username, 'insert')

    @dp.message_handler(Text(equals='УВЕДОМЛЕНИЕ КИТАЙ'))
    async def notification_china(message: types.Message):
        column = 'is_sent_china'
        message_temp = 'Дата отправки с Китая в Казахстан'
        sql = f"""select distinct chat_id from user_truck_info where is_paid=True"""
        df = get_data_from_db(sql)
        token = os.environ.get("BOT_TOKEN")
        for id in df.chat_id.tolist():
            sql_1 = f"""select truck_code, added_date from truck_info where truck_code in (select truck_code 
                        from user_truck_info where chat_id={id} and is_paid=True) and {column}=False"""
            data_list = get_data_from_db(sql_1)
            if len(data_list) != 0:
                result = ''
                for index, row in data_list.iterrows():
                    result = f"{message_temp}: {row['added_date']}" \
                             f"\nТрек код: {row['truck_code']}\n"

                telegram_bot_sendtext(token, str(result), id)

                sql = f"""update truck_info
                          set {column}=True
                            where truck_code in ({str(data_list.truck_code.tolist())[1:-1]})"""
                b.update_truck_info(sql)

    @dp.message_handler(Text(equals='УВЕДОМЛЕНИЕ КАЗАХСТАН'))
    async def notification_china(message: types.Message):
        column = 'is_sent_kz'
        message_temp = 'Дата прибытия в Алматы'
        sql = f"""select distinct chat_id from user_truck_info where is_paid=True"""
        df = get_data_from_db(sql)
        token = os.environ.get("BOT_TOKEN")
        for id in df.chat_id.tolist():
            sql_1 = f"""select truck_code, added_date from truck_info where truck_code in (select truck_code 
                            from user_truck_info where chat_id={id} and is_paid=True) and {column}=False"""
            data_list = get_data_from_db(sql_1)
            if len(data_list) != 0:
                result = ''
                for index, row in data_list.iterrows():
                    result = f"{message_temp}: {row['added_date']}" \
                             f"\nТрек код: {row['truck_code']}\n"

                telegram_bot_sendtext(token, str(result), id)

                sql = f"""update truck_info
                              set {column}=True
                                where truck_code in ({str(data_list.truck_code.tolist())[1:-1]})"""
                b.update_truck_info(sql)

    @dp.message_handler(Text(equals='ОТКРЫТЬ ДОСТУП В CHAT_ID'))
    async def add_permission_notification(message: types.Message):
        await bot.send_message(message.from_user.id, 'Добавьте CHAT_ID')

    @dp.message_handler(Text(equals='ДОБАВИТЬ ТРЕК-КОД'))
    async def add_truck_code(message: types.Message):
        await bot.send_message(message.from_user.id, 'После добавление трек-кодов нажмите кнопку *ЗАВЕРШИТЬ*',
                               reply_markup=nav.finishMenu, parse_mode=types.ParseMode.MARKDOWN)

    @dp.message_handler(lambda message_2: message_2.text not in ['ДОБАВИТЬ ТРЕК-КОД',
                                                                 'ЗАВЕРШИТЬ', 'ГЛАВНОЕ',
                                                                 'ДОБАВЛЕННЫЕ ТРЕК-КОДЫ',
                                                                 'ОТКРЫТЬ ДОСТУП В CHAT_ID',
                                                                 'УВЕДОМЛЕНИЕ КИТАЙ',
                                                                 'УВЕДОМЛЕНИЕ КАЗАХСТАН'])
    async def adding_truck_codes_and_chat_id_permission(message_2: types.Message):
        chat_id = message_2.from_user.id
        truck_code = message_2.text
        today = date.today()
        if len(truck_code) >= 13:
            b.insert_chat_id__truck_number(chat_id, truck_code, today, kind='insert')
            await bot.send_message(message_2.from_user.id, f'Трек-код добавлен: *{truck_code}*'
                                                           f'\nПосле добавление трек-кодов нажмите кнопку *ЗАВЕРШИТЬ*',
                                   reply_markup=nav.finishMenu, parse_mode=types.ParseMode.MARKDOWN)
        elif 9 <= len(truck_code) <= 12 and truck_code.isdigit() and chat_id == 309032069:
            b.insert_chat_id_permission(int(truck_code))
            await bot.send_message(message_2.from_user.id, f'Доступ для CHAT_ID={int(truck_code)} открыт')

        else:
            await bot.send_message(message_2.from_user.id, 'Трек-код не правильный')

    @dp.message_handler(Text(equals='ГЛАВНОЕ'))
    async def open_permission(message: types.Message):
        user_id = message.from_user.id
        if user_id != 309032069:
            await bot.send_message(message.from_user.id, '*ГЛАВНОЕ*',
                                   reply_markup=nav.mainMenu, parse_mode=types.ParseMode.MARKDOWN)
        else:
            await bot.send_message(message.from_user.id, '*ГЛАВНОЕ*',
                                   reply_markup=nav.nurgul_button, parse_mode=types.ParseMode.MARKDOWN)

    @dp.message_handler(Text(equals='ЗАВЕРШИТЬ'))
    async def finish(message: types.Message):
        chat_id = message.from_user.id
        first_name = message.from_user.first_name
        surname = message.from_user.last_name
        username = message.from_user.username
        today = date.today()

        sql = f"""select * from user_truck_info where chat_id={chat_id} and is_paid=False"""
        data = get_data_from_db(sql)
        bot_message = f'chat_id: {chat_id}' \
                      f'\nfirstname: {first_name}' \
                      f'\nlastname: {surname}' \
                      f'\nusername: {username}' \
                      f'\nВремя добавления трек-кодов: {today}' \
                      f'\nДобавил количество трек-кодов: {len(data)}' \
                      f'\nДолжен скинуть чек на сумму: {len(data) * 30} тенге'
        telegram_bot_sendtext(token_data, bot_message, 309032069)
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

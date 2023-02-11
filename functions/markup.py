from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


add_truck_code = KeyboardButton('ДОБАВИТЬ ТРЕК-КОД')
check_truck_code = KeyboardButton('ДОБАВЛЕННЫЕ ТРЕК-КОДЫ')
finish = KeyboardButton('ЗАВЕРШИТЬ')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(add_truck_code, check_truck_code)
finishMenu = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(finish)

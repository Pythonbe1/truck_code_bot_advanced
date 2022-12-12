from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainAll = KeyboardButton('ДОБАВИТЬ ТРЕК-КОД')
mainFinance = KeyboardButton('ДОБАВЛЕНЫ ТРЕК-КОДЫ')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(mainAll, mainFinance)

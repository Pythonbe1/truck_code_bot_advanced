from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

mainAll = KeyboardButton('ДОБАВИТЬ ТРЕК-КОД')

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(mainAll)


mainend = KeyboardButton('ЗАКОНЧИТЬ')
mainFinish = ReplyKeyboardMarkup(resize_keyboard=True).add(mainend)
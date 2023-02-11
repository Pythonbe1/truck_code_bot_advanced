from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard1 = InlineKeyboardMarkup()
keyboard2 = InlineKeyboardMarkup()

button1 = InlineKeyboardButton(text="ДОБАВИТЬ ТРЕК-КОД", callback_data="button1")
button2 = InlineKeyboardButton(text="ЗАКОНЧИТЬ", callback_data="button2")
keyboard1.add(button1)
keyboard2.add(button2)

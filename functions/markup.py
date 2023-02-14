from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

add_truck_code = KeyboardButton('ДОБАВИТЬ ТРЕК-КОД')
check_truck_code = KeyboardButton('ДОБАВЛЕННЫЕ ТРЕК-КОДЫ')
finish = KeyboardButton('ЗАВЕРШИТЬ')
main = KeyboardButton('ГЛАВНОЕ')
permission = KeyboardButton('ОТКРЫТЬ ДОСТУП В CHAT_ID')
china = KeyboardButton('УВЕДОМЛЕНИЕ КИТАЙ')
kz = KeyboardButton('УВЕДОМЛЕНИЕ КАЗАХСТАН')

nurgul_button = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(add_truck_code, check_truck_code,
                                                                              permission, china, kz, finish)
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(add_truck_code, check_truck_code, finish)
finishMenu = ReplyKeyboardMarkup(resize_keyboard=True, selective=True).add(finish, main)

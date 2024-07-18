import telebot

# region Keyboard Save and Change
keyboard_data = telebot.types.InlineKeyboardMarkup()
button_save = telebot.types.InlineKeyboardButton(text="Сохранить",
                                                 callback_data='save_data')
button_change = telebot.types.InlineKeyboardButton(text="Изменить",
                                                   callback_data='change_data')
keyboard_data.add(button_save, button_change)
# endregion

# region Keyboard Send location
keyboard_location = telebot.types.ReplyKeyboardMarkup()
button_location = telebot.types.KeyboardButton(text="Отправить геолокацию",
                                               request_location=True)
keyboard_location.add(button_location)
# endregion

import requests
import telebot
from config import TOKEN
from keyboards import keyboard_data, keyboard_location
from geolocation_finder import geocoder
from cost_finder import citimobil


bot = telebot.TeleBot(TOKEN)

# TODO(INCLUDE) Временный список для хранения информации о пользователях, позже надо заменить все на PostgreSQL
users = {}


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Добро пожаловать в бота <НАЗВАНИЕ>! Как вас зовут?')
    users[chat_id] = {}
    bot.register_next_step_handler(message, save_name)


# TODO(INCLUDE) Этот блок можно доработать c помощью передачи данных в 1 функцию(save) и там уже в завимости от данных
#  перекидывать и сохранять
# region Save function
def save_name(message):
    chat_id = message.chat.id
    name = message.text
    users[chat_id]['name'] = name
    bot.send_message(chat_id, f'Сохранить данные?', reply_markup=keyboard_data)


def save_surname(message):
    chat_id = message.chat.id
    surname = message.text
    users[chat_id]['surname'] = surname
    bot.send_message(chat_id, f'Сохранить данные?', reply_markup=keyboard_data)


# endregion Save function


# Get location from user and find on the map
def my_location(message):
    global actual_address
    chat_id = message.chat.id
    if message.content_type == "location":
        latitude, longitude = message.location.latitude, message.location.longitude
        actual_address = geocoder(latitude, longitude)
        bot.send_message(chat_id, f'Вы находитесь тут: {actual_address}?', reply_markup=keyboard_data)
    # TODO Не сделана проверка информации из текстового ответа
    elif message.content_type == "text":
        bot.send_message(chat_id, f'Вы находитесь тут: {message.text}?', reply_markup=keyboard_data)
    users[chat_id]['location'] = actual_address


def end_location(message):
    chat_id = message.chat.id
    if message.content_type == 'location':
        latitude, longitude = message.location.latitude, message.location.longitude
        end_address = geocoder(latitude, longitude)
        bot.send_message(chat_id, f'Ваш конечный адрес: {actual_address}?', reply_markup=keyboard_data)
    elif message.content_type == "text":
        # TODO Должен быть запрос в агрегатор по полученным данным и вывод точки, которую выдал агрегатор по этим
        #  данным (Уже можно узнать цену)
        bot.send_message(chat_id, f'в')


# region Buttons for save and change
@bot.callback_query_handler(func=lambda call: call.data == 'save_data')
def save_btn(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Данные сохранены!')
    if 'surname' not in users[chat_id]:
        bot.send_message(chat_id,
                         f'Отлично, ' + users[chat_id]['name'] + '. Теперь укажите свою фамилию')
        bot.register_next_step_handler(message, save_surname)
    elif 'location' not in users[chat_id]:
        bot.send_message(chat_id,
                         f'Отлично, ' + users[chat_id]['name'] + '. Теперь отправьте свою геолокацию',
                         reply_markup=keyboard_location)

        bot.register_next_step_handler(message, my_location)
    else:
        bot.send_message(chat_id,
                         f'Ваши данные успешно отправлены!\n\n'
                         f'*👤 ФИО:*\n {users[chat_id]["surname"]} {users[chat_id]["name"]}\n\n'
                         f'*🏠 Ваше местоположение:*\n {actual_address}\n\n'
                         f'💰 Стоимость Ситимобил: {citimobil(actual_address, "Ульяновск, Московское шоссе 108")}', parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data == 'change_data')
def change_btn(call):
    message = call.message
    chat_id = message.chat.id
    message_id = message.message_id
    bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                          text='Изменение данных!')
    if 'location' in users[chat_id]:
        del users[chat_id]['location']
        bot.register_next_step_handler(message, my_location)
    elif 'surname' in users[chat_id]:
        del users[chat_id]['surname']
        bot.register_next_step_handler(message, save_surname)
    else:
        del users[chat_id]['name']
        bot.register_next_step_handler(message, save_name)
# endregion


# TODO(INCLUDE) Кусок кода для профиля, который надо доработать в будущем
@bot.message_handler(commands=['who_i'])
def who_i(message):
    chat_id = message.chat.id
    name = users[chat_id]['name']
    surname = users[chat_id]['surname']
    bot.send_message(chat_id, f'Вы: {name} {surname}')


if __name__ == '__main__':
    bot.infinity_polling()

import telebot
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot('6607550084:AAGEAWbRbBZeqz-8uOaKTG1P8aa56GmJLHk')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https://www.bing.com/')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://www.pinterest.com')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2,btn3)
    bot.reply_to(message, 'Какое красивое фото!!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
     bot.edit_message_text('Edit  text', callback.message.chat.id, callback.message.message_id)



@bot.message_handler(['start'])
def start(message):
    conn = sqlite3.connect('ProgramII.sql')
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        pass TEXT
    )''')

    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Добро Пожаловать! Введите свое имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пороль!')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('ProgramII.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES (?, ?)", (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Приятного пользования)!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    conn = sqlite3.connect('ProgramII.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    bot.send_message(call.message.chat.id, info)

    cur.close()
    conn.close()





def on_click(message):
    if message.text == 'Перейти на сайт':
        bot.send_message(message.chat.id, 'Website is open')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Deleted')




bot.polling(none_stop=True)
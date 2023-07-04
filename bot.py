
import telebot
import sqlite3
from telebot import types

TOKEN = '5831219596:AAE_neHWLDwcQbwmkYntD7CX-pRbunxHc5g'
bot = telebot.TeleBot(TOKEN)
global name
global password
@bot.message_handler(commands=['start'])
def start(message):
	conn = sqlite3.connect('base.db')
	cur = conn.cursor()
	prov = cur.execute('SELECT COUNT(*) FROM users WHERE user_id = (?)', (message.from_user.id,)).fetchall
	if (prov == 0 ):
		cur.execute('INSERT INTO users (user_id) VALUES (?)', (message.from_user.id,))
	conn.commit()
	cur.close()
	conn.close()
	markup = types.InlineKeyboardMarkup()
	btn1 = types.InlineKeyboardButton('1', callback_data = 'bt1')
	btn2 = types.InlineKeyboardButton('2', callback_data = 'bt2')
	btn3 = types.InlineKeyboardButton('3', callback_data = 'bt3')
	btn4 = types.InlineKeyboardButton('4', callback_data = 'bt4')
	btn5 = types.InlineKeyboardButton('5', callback_data = 'bt5')
	markup.row(btn1)
	markup.row(btn2, btn3)
	markup.row(btn4, btn5)
	bot.send_message(message.chat.id, 'Выберите номер задания', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
	conn = sqlite3.connect('base.db')
	cur = conn.cursor()
	for i in range(1,6):
		if (callback.data == 'bt' + str(i)):
			strr = cur.execute('SELECT task FROM tasks WHERE task_id = (?)', (i,))
			bot.send_message(callback.message.chat.id, strr)
			bot.delete_message(callback.message.chat.id, callback.message.message_id)

	conn.commit()
	cur.close()
	conn.close()

	# markup = types.InlineKeyboardMarkup()
	# btn1 = types.InlineKeyboardButton('Зарегистрироваться', callback_data = 'reg')
	# markup.row(btn1)
	# btn2 = types.InlineKeyboardButton('Авторизироваться', callback_data = 'auth')
	# markup.row(btn2)
	# bot.send_message(message.chat.id, 'Привет!1', reply_markup=markup)

# @bot.callback_query_handler(func=lambda callback: True)
# def callback_message(callback):
# 	if (callback.data == 'reg'):
# 		bot.send_message(callback.message.chat.id, 'Введите имя пользователя' )
# 		bot.register_next_step_handler(callback, user_name)
		# global name 
		# name = callback.message.text.strip()

		# bot.send_message(callback.message.chat.id, 'Введите пароль' )
		# global password
		# password = callback.message.text.strip()
		# callback.cur.execute("INSERT INTO users (name, password) VALUES ('%s', '%s')" %(name,password))

# def user_name(message):
# 	global name
# 	name = message.text.strip()
# 	message.bot.send_message(message.chat.id, 'Введите пароль')
# 	message.register_next_step_hadler(message, user_pass)

# def user_pass(message):
# 	global password
# 	password = message.text.strip()
# 	conn = sqlite3.connect('base.sql')
# 	cur = conn.cursor()
# 	cur.execute("INSERT INTO users (name, password) VALUES ('%s', '%s')" %(name,password))
# 	conn.commit()
# 	cur.close()  


	# conn.close()
	# message.bot.send_message(message.chat.id, 'Введите пароль')
	# message.register_next_step_hadler(message, user_pass)

	 
bot.polling(none_stop=True)   
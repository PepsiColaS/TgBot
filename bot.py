import telebot
import sqlite3
from telebot import types
from tasks_checker import TaskChecker
import re
from telegram.ext import Updater, CommandHandler
n = 1
tempr = -1
idtask = -1
idperson = -1

TOKEN = '5831219596:AAE_neHWLDwcQbwmkYntD7CX-pRbunxHc5g'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
	global n
	conn = sqlite3.connect('base.db')
	cur = conn.cursor()
	prov = cur.execute('SELECT COUNT(*) FROM users WHERE user_id = (?)', (message.from_user.id,))

	if (prov == 0 ):
		cur.execute('INSERT INTO users (user_id) VALUES (?)', (message.from_user.id,))
	global idperson 
	idperson = cur.execute('SELECT (id) FROM users WHERE user_id =(?)',(message.from_user.id,))

	conn.commit()
	cur.close()
	conn.close()
	
	markup = types.InlineKeyboardMarkup()
	btn = types.InlineKeyboardButton('Поехали!', callback_data = str(n))
	markup.row(btn)
	bot.send_message(message.chat.id, "Привет! Я бот который поможет тебе проверить знания в it. Ты готов?",  reply_markup=markup)
	# bot.send_message(message.chat.id, 'Вот твое задание', reply_markup=markup)
	# btn2 = types.InlineKeyboardButton('2', callback_data = 'bt2')
	# btn3 = types.InlineKeyboardButton('3', callback_data = 'bt3')
	# btn4 = types.InlineKeyboardButton('4', callback_data = 'bt4')
	# btn5 = types.InlineKeyboardButton('5', callback_data = 'bt5')
	# markup.row(btn1, btn2)
	# markup.row(btn3, btn4)
	# markup.row(btn4, btn5)
	# bot.send_message(message.chat.id, 'Выберите номер задания', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
	global n
	conn = sqlite3.connect('base.db')
	cur = conn.cursor()
	for i in range(n,6):
		if (callback.data == str(i)):
			global tempr
			tempr = i
			strr = cur.execute('SELECT task FROM tasks WHERE task_id = (?)', (i,))
			bot.send_message(callback.message.chat.id, strr)
			bot.delete_message(callback.message.chat.id, callback.message.message_id)
			n += 1
			bot.register_next_step_handler(callback.message,  otv)	
			# idtask = i	
		

	conn.commit()
	cur.close()
	conn.close()

def otv(message):
	global tempr
	global n
	# max
	if (tempr == 1):
		user_solution = message.text
		test_cases = [
		([0, 2, 3, 4, 5], 5),
		([-1, -5, 0, -10], 0),
		([100, 200, 50, 300], 300),
		([0, 0, 0, 0], 0),
		]
		bot.send_message(message.chat.id,TaskChecker(user_solution, test_cases).check())
		markup = types.InlineKeyboardMarkup()
		btn = types.InlineKeyboardButton('Дальше!', callback_data = str(n))
		markup.row(btn)
		bot.send_message(message.chat.id, "Ответ принят!",  reply_markup=markup)
	# min
	if (tempr == 2):
		user_solution = message.text
		test_cases = [
		([0, 2, 3, 4, 5], 0),
		([-1, -5, 0, -10], -10),
		([100, 200, 50, 300], 50),
		([0, 0, 0, 1], 0),
		]
		bot.send_message(message.chat.id,TaskChecker(user_solution, test_cases).check())
		markup = types.InlineKeyboardMarkup()
		btn = types.InlineKeyboardButton('Дальше!', callback_data = str(n))
		markup.row(btn)
		bot.send_message(message.chat.id, "Ответ принят!",  reply_markup=markup)
	# +
	if (tempr == 3):
		user_solution = message.text
		test_cases = [
		([0, 2, 3, 4, 5], 14),
		([-1, -5, 0, -10], -16),
		([100, 200, 50, 300], 650),
		([0, 0, 1, 1], 2),
		]
		bot.send_message(message.chat.id,TaskChecker(user_solution, test_cases).check())
		markup = types.InlineKeyboardMarkup()
		btn = types.InlineKeyboardButton('Дальше!', callback_data = str(n))
		markup.row(btn)
		bot.send_message(message.chat.id, "Ответ принят!",  reply_markup=markup)
	# *
	if (tempr == 4):
		user_solution = message.text
		test_cases = [
		([0, 2, 3, 4, 5], 120),
		([-1, -5, 0, -10], -50),
		([1, 2, 5, 3], 30),
		([1, 1, 3, 2], 6),
		]
		bot.send_message(message.chat.id,TaskChecker(user_solution, test_cases).check())
		bot.send_message(message.chat.id, "Ты молодец! Но тебе есть куда расти!")

	# conn = sqlite3.connect('base.db')
	# cur = conn.cursor()
	# cur.execute('INSERT INTO tasks (correct) WHERE user_id = (?)', (idperson,))



	# bot.send_message(message.chat.id, message.text)	



bot.polling(none_stop=True) 
    

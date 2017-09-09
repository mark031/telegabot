import telebot, datetime, text_commands, school_mosreg, cookies_bd, json, requests
token = '424339878:AAFnqFvla2o1BL9dVcmb29Bsz42h-jZh4ig'
bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
	if message.chat.id in [331009265, 264432579]:
		if message.text.lower()[0:6] == 'логин ':
			if cookies_bd.find_one(message.chat.id):
				bot.send_message(message.chat.id, 'Вы уже авторизованы')
			else:
				if len(message.text[6:len(message.text)].split(' ')) == 2:
					cookie = school_mosreg.login(*message.text[6:len(message.text)].split(' '))
					if 'DnevnikLoadTestAuth_a' in cookie.keys():
						cookies_bd.insert_one(message.chat.id, cookie)
						bot.send_message(message.chat.id, 'Авторизация завершена')
					else:
						bot.send_message(message.chat.id, 'Ошибка авторизации')
				else:
					bot.send_message(message.chat.id, 'Комманда задана некорректно')
		elif message.text.lower() == 'расписание':
			bot.send_message(message.chat.id, "На какой день?", reply_markup=text_commands.schedule('marks'))
		elif message.text.lower() == 'выход':
			if not cookies_bd.find_one(call.message.chat.id):
				bot.send_message(message.chat.id, 'Вы не авторизованы')
			else:
				keyboard = telebot.types.InlineKeyboardMarkup()
				keyboard.add(telebot.types.InlineKeyboardButton(text='Да', callback_data='logout'))
				bot.send_message(message.chat.id ,'Вы уверены, что хотите выйти?')
	else:
		print(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
	if call.message.chat.id in [331009265, 264432579]:
		if call.data == 'logout':
			cookies_bd.delete_one(call.message.chat.id)
			bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Выход завершен')
		else:
			cookie = cookies_bd.find_one(call.message.chat.id)
			if cookie:
				date = datetime.datetime.strptime(call.data[0:10], '%Y-%m-%d').date()
				if call.data[10:20] == 'marks':
					text = school_mosreg.parsing_marks(school_mosreg.mondayAtThisWeek(date), requests.utils.cookiejar_from_dict(cookie))
				elif call.data[10:20] == 'view':
					text = school_mosreg.parsing_view(school_mosreg.mondayAtThisWeek(date), requests.utils.cookiejar_from_dict(cookie))

				if text:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = text_commands.allLesson(text[str(date)], call.data[10:20], date))
				else:
					bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Расписание отсутствует')
			else:
				bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = 'Вы не авторизованы')
if __name__ == '__main__':
	bot.polling(none_stop = True)

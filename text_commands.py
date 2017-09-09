import telebot, datetime, school_mosreg, cookies_bd

def days(date_now):
	week = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
	ret = []
	i = 0
	for day in week:
		if datetime.datetime.weekday(date_now + datetime.timedelta(i)) == 6:
			i += 1
		day_date = date_now + datetime.timedelta(i)
		ret += [[str(day_date), week[datetime.datetime.weekday(day_date)] + '({month},{day})'.format(month = day_date.month, day = day_date.day)]]
		i += 1
	return ret

def schedule(add_to_end,sched = days(datetime.datetime.now().date())):
	keyboard = telebot.types.InlineKeyboardMarkup()
	row = []
	for command in sched:
		row += [telebot.types.InlineKeyboardButton(text=command[1], callback_data=command[0] + add_to_end)]
		if len(row) == 3:
			keyboard.row(*row)
			row = []
	return keyboard

def nextLesson(chat_id):
	cookies = cookies_bd.find_one(chat_id)
	schedule = school_mosreg

def allLesson(allLesson, typeOfLessons, date):
	week = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу']
	ret = 'Расписание на ' + week[datetime.datetime.weekday(date)] + '({date.year}/{date.month}/{date.day})'.format(date = date) + '\n----------------------------------------\n'
	if allLesson == {}:
		ret += 'Уроков нет'
	else:
		if typeOfLessons == 'marks':
			for lesson in allLesson:
				ret += '{number}:\n{lessonName}'.format(number = allLesson[lesson]['number'], lessonName = allLesson[lesson]['name'])
				if allLesson[lesson]['homework']:
					ret += '\nДомашнее задание: ' + allLesson[lesson]['homework']
				if allLesson[lesson]['mark']:
					ret += '\nОценка за урок: ' + allLesson[lesson]['mark']
				ret += '\n----------------------------------------\n'
		elif typeOfLessons == 'view':
			for lesson in allLesson:
				ret += '{number} урок:\n{lessonName}\nУчитель: {teacherName}\nВремя: {lessonTime}\nКабинет: {room}'.format(number = lesson, lessonName = allLesson[lesson][0]['name'], teacherName = allLesson[lesson][0]['teacher'], lessonTime = allLesson[lesson][0]['time'], room = allLesson[lesson][0]['location'])
				if (len(allLesson[lesson]) - 1):
					ret += '- - - - - - - - - - - - - - - - - - - -\n{lessonName}\nУчитель: {teacherName}\nВремя: {lessonTime}\nКабинет: {room}'.format(number = lesson, lessonName = allLesson[lesson][1]['name'], teacherName = allLesson[lesson][1]['teacher'], lessonTime = allLesson[lesson][1]['time'], room = allLesson[lesson][0]['location'])
				ret += '\n----------------------------------------\n'
	return ret

commands = {
	'расписание': schedule,
	'следующий урок': nextLesson
}
# -*- coding: utf-8 -*-
import requests, datetime
from bs4 import BeautifulSoup
headers = {
	'Connection': 'keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.92 Safari/537.36 42885',
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate, sdch, br',
	'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
	'X-Compress': 'null'
}

def datenow(date = datetime.date):
	a = str(date)
	i = 0
	ret = ''
	while i < len(a):
		if a[i] in '1234567890': ret += a[i]
		i += 1
	return ret

def parsing_view(mondayAtThisWeek, cookies):
	ident = {'Пед': 'teacher', 'Вре': 'time', 'Мес': 'location'}
	s = requests.Session()
	s.cookies.update(cookies)
	s.headers.update(headers)
	rtext = s.get('https://schools.school.mosreg.ru/schedules/view.aspx?year={year}&month={month}&day={day}'.format(year = mondayAtThisWeek.year, month = mondayAtThisWeek.month, day = mondayAtThisWeek.day)).text
	idEditor = BeautifulSoup(rtext, 'lxml').find('table', {'id':'editor'})
	if idEditor == None:
		return None
	allWWeek = idEditor.findAll('tr', {'class':'wWeek'})
	i = 1
	j = 0
	lessons = {}
	while j < 7:
		lessons[str(mondayAtThisWeek + datetime.timedelta(j))] = {}
		j += 1

	i = 1
	for WWeek in allWWeek:
		j = 1
		while j < 8:
			WWeakTD = WWeek.find('td', {'id': ('d' + str(datenow(mondayAtThisWeek + datetime.timedelta(j - 1))) + '_' + str(i))})
			#print(WWeakTD)
			if WWeakTD.find('a') != None:
				k = 0
				lessons[str(mondayAtThisWeek + datetime.timedelta(j - 1))][i] = []
				for dl in WWeakTD.findAll('div', {'class':'dL '}):
					lessons[str(mondayAtThisWeek + datetime.timedelta(j - 1))][i] += [{'name':dl.find('a').text}]
					for p in dl.findAll('p'):
						lessons[str(mondayAtThisWeek + datetime.timedelta(j - 1))][i][k][ident[str(p)[10:13]]] = p.text
					k += 1
			j += 1
		i += 1

	return lessons

def parsing_marks(mondayAtThisWeek, cookies):
	s = requests.Session()
	s.cookies.update(cookies)
	s.headers.update(headers)
	j = 0
	lessons = {}
	while j < 7:
		lessons[str(mondayAtThisWeek + datetime.timedelta(j))] = {}
		j += 1
	rtext = s.get('https://schools.school.mosreg.ru/marks.aspx?school=10686&tab=week&year={year}&month={month}&day={day}'.format(year = mondayAtThisWeek.year, month = mondayAtThisWeek.month, day = mondayAtThisWeek.day)).text
	#diarydays = BeautifulSoup(rtext, 'lxml').find('div', {'id':'diarydays'})
	#diarydaysleft = diarydays.find('div', {'id':'diarydaysleft'})
	#diarydaysright = diarydays.find('div', {'id':'diarydaysright'})
	allPBC = BeautifulSoup(rtext, 'lxml').findAll('div', {'class':'panel blue2 clear'})
	if not allPBC:
		return None
	j = 0
	i = 0
	for day in allPBC:
		i = 0
		for tr in day.findAll('tr'):
			name = tr.find('a', {'class': 'strong '}).text
			number = tr.find('div', {'class': 'light'}).text
			homework = tr.find('a', {'target': '_blank'})
			mark = tr.find('span', {'class':'mark mG analytics-app-popup-mark'})
			lessons[str(mondayAtThisWeek + datetime.timedelta(j))][i] = {
				'name': name,
				'number': number,
				'homework': None if not homework else homework.text.replace('\n', ' '),
				'mark': None if not mark else mark.text
				}
			i += 1
		j += 1
	return lessons

def login(login, password):
	s = requests.Session()
	s.headers.update(headers)
	return requests.utils.dict_from_cookiejar(s.post('https://login.school.mosreg.ru/user/login', {'login':login, 'password':password}).cookies)

def mondayAtThisWeek(dtn):
	mondayAtThisWeek = datetime.date(dtn.year, dtn.month, dtn.day - datetime.datetime.weekday(dtn))
	return mondayAtThisWeek
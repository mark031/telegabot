import pymongo
client = pymongo.MongoClient('mongodb://mark_031:182309db@ds125914.mlab.com:25914/lob9mr')
cookies = client.lob9mr.cookies

def insert_one(chat_id, cookie):
	cookies.insert_one({'id' : chat_id, 'cookies' : cookie})

def find_one(chat_id):
	ret = cookies.find_one({'id' : chat_id})
	if ret:
		return ret['cookies']
	else:
		return None

def delete_one(chat_id):
	return cookies.delete_one({'id' : chat_id}).deleted_count
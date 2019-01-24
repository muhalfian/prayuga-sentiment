import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import needed.db_mysql as db_mysql
import helper.preprocessing as preprocessing
import analyzer.impress as impress
from datetime import datetime

def saveComment(data_save):
	content = data_save['text_comment']
	id_apps = data_save['id_apps']
	time    = data_save['date']
	sosmed  = data_save['sosmed']
	user    = data_save['name']
	id_url  = data_save['id_url']
	keyword = preprocessing.do(content);
	dataProcess  = impress.play(keyword,id_apps);
	sentiment    = dataProcess['sentiment'];
	# for view counting rule impressi
	recordCounting = preprocessing.recordCounting(dataProcess);
	arr_word       = recordCounting['arr_word'];
	arr_counted    = recordCounting['arr_counted'];
	arr_score      = recordCounting['arr_score'];
	role_group     = recordCounting['role_group'];

	if(checkExists(id_apps,id_url,time)):
		print content;
		print "::"+str(sentiment);
		print "===============================";
		try:
			sql = '''INSERT INTO apps_opinion(id_apps, sentiment, content, time, sosmed, user, arr_word, arr_counted, arr_score, role_group, id_url) 
									VALUES ('%d',   '%s',      '%s',    '%s', '%d',  '%s',   '%s',      '%s',        '%s',       '%s',    '%s')''' \
					% (id_apps, sentiment, str(content), time, sosmed, user, arr_word, arr_counted, arr_score, role_group, id_url);
			db_mysql.executeSql(sql);
			db_mysql.commit();pass
		except Exception as e:
			pass

def checkExists(id_apps,id_url,time):
	sql = 'SELECT * FROM apps_opinion WHERE id_apps='+str(id_apps)+' AND id_url="'+str(id_url)+'" AND time="'+str(time)+'"';
	db_mysql.executeSql(sql);
	data = db_mysql.fetch('one');
	if(data == None):
		return True;
	return False;

def checkNewsIsMatch(title,keywords):
	title = title.lower();
	for keyword in keywords:
		if(keyword.lower() in title):
			return True;
	return False;

def checkValidDate(news_date,since,until):
	if(until == None):
		until = datetime.now();

	news_date = datetime.strptime(news_date, '%d %b %Y %H:%M');
	since     = datetime.strptime(since, "%Y-%m-%d");
	until     = datetime.strptime(until, "%Y-%m-%d");

	if(news_date >= since and news_date <= until):
		return True
	return False
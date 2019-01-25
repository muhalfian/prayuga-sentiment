import MySQLdb

hostname = "localhost"
username = "root"
password = "labkdd123"
db_name  = "prayuga"

# Open database connection
db = MySQLdb.connect(hostname,username,password,db_name)
db.set_character_set('utf8')

# prepare a cursor object using cursor() method
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

def executeSql(sql):
	return cursor.execute(sql);

def fetch(type='all'):
	if type=='all':
		return cursor.fetchall();
	else:
		return cursor.fetchone();
def commit():
	db.commit();

def escapeString(string):
	return MySQLdb.escape_string(string);

def insertOpini(data):
	var_content       = data['content'];
	var_time          = data['time'];
	var_location      = data['location'];
	var_sosmed_source = data['sosmed'];
	var_user          = data['user'];
	var_keyword       = data['keyword'];
	var_sentiment     = data['sentiment'];

	sql = '''INSERT INTO opini(sentiment,content,time,location,sosmed_source,user,keyword)
			VALUES ('%s','%s','%s','%s','%d','%s','%s')''' \
			% (var_sentiment, var_content, var_time, var_location, var_sosmed_source, var_user, var_keyword);
	cursor.execute(sql);
	db.commit()

def insertOpini2(data,sentiment):
	var_content       = MySQLdb.escape_string(data['content']);
	var_time          = data['time'];
	var_location      = data['location'];
	var_sosmed_source = data['sosmed'];
	var_user          = data['user'];
	var_keyword       = data['keyword'];

	sql = '''INSERT INTO opini(sentiment,content,time,location,sosmed_source,user,keyword)
			VALUES ('%s','%s','%s','%s','%d','%s','%s')''' \
			% (sentiment,var_content, var_time, var_location, var_sosmed_source, var_user, var_keyword);
	cursor.execute(sql);
	db.commit()

def existSentimentalWord(word):
	sql = '''SELECT *
				FROM memory_word
				WHERE word="%s" AND type is not NULL AND value is not NULL''' \
				% (word);
	cursor.execute(sql);
	return cursor.fetchone();

def existSentimentalWordMainObject(word,idApps=None):
	if(idApps != None):
		if(idApps == 'eval'):
			sql = '''SELECT *
						FROM eval_memory_word
						WHERE word="%s" AND value is not NULL''' \
						% (word);
		else:
			sql = '''SELECT *
						FROM apps_memory_word
						WHERE word="%s" AND id_apps=%d AND value is not NULL''' \
						% (word,idApps);
		cursor.execute(sql);
		return cursor.fetchone();

def existOtherKamus(word):
	sql = '''SELECT *
				FROM tb_katadasar
				WHERE word="%s"''' \
				% (word);
	cursor.execute(sql);
	return cursor.fetchone();

def insertUnknownWord(word):
	if len(word) < 20:
		sql = '''SELECT *
					FROM unknown_word
					WHERE word="%s"''' \
					% (word);
		cursor.execute(sql);
		result = cursor.fetchone();
		if result == None:
			sql = '''INSERT INTO unknown_word(word)
						VALUES ('%s')'''\
						% (word);
			cursor.execute(sql);
			db.commit();
		else:
			new_frequent = result[4] + 1;
			sql = '''UPDATE unknown_word SET frequently=%d
						WHERE id=%d ''' % (new_frequent,result[0]);
			cursor.execute(sql);
			db.commit();

def existStoplist(word):
	sql = '''SELECT *
				FROM memory_stopword
				WHERE word="%s"''' \
				% (word);
	cursor.execute(sql);
	return cursor.fetchone();

def migrasi():
	sql = '''SELECT *
				FROM tb_katadasar''';
	cursor.execute(sql);
	result = cursor.fetchall();
	return result;

def updateMigrasi(id,new_val):
	sql = '''UPDATE tb_katadasar SET value=%d
			WHERE id=%d ''' % (new_val,id);
	cursor.execute(sql);
	db.commit()

def insertOldTweet(data):
	var_content       = data['content'];
	var_time          = data['time'];
	var_keyword       = data['keyword'];
	db_dict = {'content':var_content, 'time':var_time, 'keyword':var_keyword};
	sql = "INSERT INTO old_opini(text,time,keyword) VALUES (%(content)s,%(time)s,%(keyword)s)";
	cursor.execute(sql, db_dict);
	db.commit()

def insertWord(word):
	var_word       = word;
	db_dict = {'word':var_word};
	sql = "INSERT INTO mining_dict(word) VALUES (%(word)s)";
	cursor.execute(sql, db_dict);

def getAllDict():
	sql = '''SELECT *
				FROM mining_dict_en''';
	cursor.execute(sql);
	result = cursor.fetchall();
	return result;

def getMemoryGroupWord():
	sql = '''SELECT word
				FROM memory_word WHERE word LIKE "% %"''';
	cursor.execute(sql);
	result = cursor.fetchall();
	return result;

def getOtherMemoryGroupWord():
	sql = '''SELECT word
				FROM apps_memory_word WHERE word LIKE "% %"''';
	cursor.execute(sql);
	result = cursor.fetchall();
	return result;

def checkExistSentiwn(word):
	sql = '''SELECT *
				FROM sentiwn_en
				WHERE word="%s"''' \
				% (word);
	cursor.execute(sql);
	return cursor.fetchone();

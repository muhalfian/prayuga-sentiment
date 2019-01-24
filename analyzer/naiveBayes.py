from __future__ import division
import needed.db_mysql as db_mysql
import helper.preprocessing as preprocessing

totalNaive = {'positif':0,'negatif':0,'netral':0,'data':0};

def initial():
	global totalNaive;

	sql = '''SELECT count(*)
				FROM eval_opinion WHERE training = 1''';
	db_mysql.executeSql(sql);
	result = db_mysql.fetch('all');
	totalNaive['positif'] = result[0][0];

	sql = '''SELECT count(*)
				FROM eval_opinion WHERE training = -1''';
	db_mysql.executeSql(sql);
	result = db_mysql.fetch('all');
	totalNaive['negatif'] = result[0][0];

	sql = '''SELECT count(*)
				FROM eval_opinion WHERE training = 0''';
	db_mysql.executeSql(sql);
	result = db_mysql.fetch('all');
	totalNaive['netral'] = result[0][0];

	totalNaive['data'] = totalNaive['positif'] + totalNaive['negatif'] + totalNaive['netral'];

def probably(word,senti):	
	global totalNaive;

	sql = 'SELECT count(*) FROM eval_opinion WHERE training = '+str(senti)+' AND content LIKE "%'+word+'%"';
	db_mysql.executeSql(sql);
	inWord = db_mysql.fetch('all')[0][0];

	if(senti == 1):
		return (inWord/totalNaive['positif']) * (totalNaive['positif']/totalNaive['data']);
	elif(senti == -1):
		return (inWord/totalNaive['negatif']) * (totalNaive['negatif']/totalNaive['data']);
	elif(senti == 0):
		return (inWord/totalNaive['netral']) * (totalNaive['netral']/totalNaive['data']);


def counting(word):
	pPos    = probably(word,1);
	pNeg    = probably(word,-1);
	pNetral = probably(word,0);
	
	if(pPos >= pNeg):
		if(pPos >= pNetral):
			result = 1;
		else:
			if(pNeg >= pNetral):
				result = -1;
			else:
				result = 0;
	elif(pNeg >= pNetral):
		result = -1;
	else:
		result = 0;

	# print pPos;
	# print pNeg;
	# print pNetral;
	# print result;
	# print "===========";
	return result;

def play(sentence):
	sentiment = 0;
	for word in sentence:
		sentiment = sentiment + counting(word);
	
	if(sentiment > 0):
		return 1;
	elif(sentiment < 0):
		return -1;
	else:
		return 0;
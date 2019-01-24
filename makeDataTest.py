import needed.db_mysql as db_mysql
import helper.preprocessing as preprocessing
import analyzer.impress as impress;

def analyzeSentiment():
	sql = '''SELECT * 
				FROM data_test''';
	
	db_mysql.executeSql(sql);
	result = db_mysql.fetch('all');
	
	for data in result:
		kalimat   = data[2];
		keyword   = preprocessing.do(kalimat);
		sentiment = impress.play(keyword)['sentiment'];
		print "==========================\n\nID: "+str(data[0])+"\n"+kalimat+"\n--Sentiment: "+str(sentiment)+"\n";

		sql = '''UPDATE data_test SET sentiment=%d 
						WHERE id=%d ''' % (sentiment,data[0]);
		db_mysql.executeSql(sql);
		db_mysql.commit();

analyzeSentiment();
import db_mysql
import collections

''' mengecek persamaan dengan sentiwn'''
# words = db_mysql.getAllDict();
# i = 0;
# for word in words:
#     result = db_mysql.checkExistSentiwn(word[1]);
#     if (result != None):
#         print result[4];
#         i = i+1;
# print i;

sql = '''SELECT * 
		FROM mining_dict_en WHERE value is NULL''';
db_mysql.executeSql(sql);
words = db_mysql.fetch('all');
ii = 0
for word in words:
	typeword = word[2];
	idword = word[0];
	word = word[1];
	sql = '''SELECT * 
			FROM sentiwn_en
			WHERE word="%s"''' \
			% (word);
	rowcount = db_mysql.executeSql(sql);
	if rowcount != 0:
		ii = ii + 1;
		print typeword;
		result = db_mysql.fetch('all');
		types = [];
		for x in result:
			types.append(x[0]);
		type_pos = collections.Counter(types).most_common(1)[0][0];
		print type_pos;
		v_pos = 0;
		v_neg = 0;
		value = 0;
		for x in result:
			if (x[0] == type_pos):
				v_pos = v_pos+x[2];
				v_neg = v_neg+x[3];

		if (v_pos > v_neg):
			if (v_pos > 0.125):
				value = 1;
		elif (v_neg > v_pos):
			if (v_neg > 0.125):
				value = -1;
		
		print types;
		print str(idword)+"."+word+" - "+type_pos+" - "+str(v_pos)+" - "+str(v_neg)+" - "+str(value);
		if (typeword == None):
			sql = '''UPDATE main_dict SET value=%d, type="%s" 
			WHERE id=%d''' % (value,type_pos,idword);
		else:
			sql = '''UPDATE main_dict SET value=%d 
			WHERE id=%d''' % (value,idword);
		print sql;
		db_mysql.executeSql(sql);
db_mysql.commit();
print ii;
	# for x in counter.most_common(1):
	# 	# print x[0];
	# 	sql = '''SELECT * 
	# 		FROM sentiwn_indo
	# 		WHERE word="%s" AND pos="%s"''' \
	# 		% (word,x[0]);
	# 	db_mysql.executeSql(sql);
	# 	result = db_mysql.fetch('all');
	# 	if result!=None:
	# 		v_pos = 0;
	# 		v_neg = 0;
	# 		value = 0;
	# 		for x in result:
	# 			v_pos = v_pos+x[2];
	# 			v_neg = v_neg+x[3];

	# 		if (v_pos > v_neg):
	# 			if (v_pos > 0.125):
	# 				value = 1;
	# 		elif (v_neg > v_pos):
	# 			if (v_neg > 0.125):
	# 				value = -1;
			
	# 		print types;
	# 		print word+" - "+x[0]+" - "+str(value);
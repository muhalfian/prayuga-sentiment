from conFile import ConFile;
import db_mysql
import preprocessing;

import operator 
from operator import itemgetter
import json
from collections import Counter

confile = ConFile();
data    = confile.readFile('data/tes.csv',';');
del data[0];
count_all = Counter()
word_berita = ['... http', '#BreakingNews', '#News', '@TribunRakyat', '#PopulerB1'];
print "start....";
for x in data:
	tweet = preprocessing.do(data[x][4]);
	if not any(word in tweet for word in word_berita):
		terms_all = [term for term in tweet];
    	count_all.update(terms_all)
# terms_all = [term for term in preprocessing.do(data[66941][4])];
# print terms_all;
p = sorted(count_all.items());

treshold = 10;
i = 0;
for x in p:
	if(x[1] >= treshold):
		if(len(x[0]) <= 25):
			# db_mysql.insertWord(x[0]);
			print x[0]+" : "+str(x[1]);
			i = i+1;
# 	# if i == 255:
# 	# 	print len(x);
# 	# if i == 256:
# 	# 	print len(x);
# 	# i = i+1;
	# if len(x) < 70:
	# 	db_mysql.insertWord(x);
	# keyword = preprocessing.do(data[x][4]);
	# date 	= data[x][1]+":00"
	# data_input = {
	# 	"content"  : data[x][4],
	# 	"time"     : date,
	# 	"keyword"  : keyword,
	# };
	# db_mysql.insertOldTweet(data_input);
	# print data[x][4];
	# print keyword;
# db_mysql.commit();
# print i;
# print data[1362][4];
#keyword = preprocessing.do(data[1362][4]);
# print keyword;
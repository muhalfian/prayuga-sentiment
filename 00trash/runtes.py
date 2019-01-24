import tweepy
import json
import datetime;
import re;

import db_mysql
import preprocessing;
import role;
import naiveBayes;

from tweepy import Stream
from tweepy.streaming import StreamListener
from pprint import pprint
from tweepy import OAuthHandler
#from twitterscraper import query_tweets
 
consumer_key    = '30KgZnTiKCOYx8oPvlKeTyGJU'
consumer_secret = '43IHxBzgaVIB3bP95ORS2wfpQxs10R7fWsTU1FftVH7WQeMFMj'
access_token    = '595044868-NaibzrBxR7kCUZm9Qgosh6DCVnnOjaHZSest4eRb'
access_secret   = 'A1hPGJ1fIV4r8zLNMdapaaXQDG5OlI5L8u04rUtrqMMSF'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
class MyListener(StreamListener):
 
    def on_data(self, tweet):
        try:
        	if 'retweeted_status' not in tweet:
        		self.dataInput(tweet);
        		return True;
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

    def dataInput(self,tweet):
        word_berita = ['... http', '#BreakingNews', '#News', '@TribunRakyat', '#PopulerB1','https'];
    	data = json.loads(tweet);
        if not any(word in data for word in word_berita):
        	# print data['text'].encode('utf-8');
        	keyword    = preprocessing.do(data['text'].decode().encode('utf-8'));
         	sentiment  = role.play(keyword);
         	print sentiment,"=>",data['text'].decode().encode('utf-8');
         	# print sentiment;
        	data_input = {
        		"content"  : data['text'].decode().encode('utf-8'),
        		"time"     : datetime.datetime.fromtimestamp(int(data['timestamp_ms'])/1000),
        		"location" : data['user']['location'],
        		"sosmed"   : 1,
        		"user"     : data['user']['screen_name'],
        		"keyword"  : keyword,
        	};
        	db_mysql.insertOpini2(data_input,sentiment);

# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=["kebijakan pemerintah"])
# kalimat = "administrasi mengalahkan ahok dengan buruk";
# kalimat = "ahok justru membangun administrasi";
# kalimat = "ahok justru membangun ahok";
# kalimat = "ahok justru membangun akibat";
# kalimat = "ahok justru mengalahkan ahok";
# kalimat = "2017 Penganguran Bertambah Akibat Dampak Dari Kebijakan Mentri Perikanan Yang Melaramg Ijin Cantrang #SaveCantrang @jokowi @Pak_JK";
# kalimat = "@jokowi @kemkominfo .. Mr.Presiden, kebijakan bebas visa kiranya perlu ditinjau ulang...selektif dan jangan diobral...";
# kalimat = "Pagi Pak @jokowi sepertinya kebijakan bebas visa bagi Cina lebih banyak merugikan Indonesia. Mgkn sudah saatnya Anda mencabut kebijakan tsb pic.twitter.com/klIQvP2jZj";
# kalimat = "tepat sekali kebijakan yang akan diambil Pres Jokowi , dimana akan segera memberikan ijin kepada asing utk memiliki properti di Indonesia.";
# kalimat = "Pak @jokowi tolong cabut tu kebijakan ,kalau gak mau mending terang terangan masukin tu semua orang China ke Indonesia https:// twitter.com/bg_marone/stat us/807002140992421888";
# kalimat = "Jgn trlalu fokus dgn Ahoax sj...sementara berjuta juta Ahoax yg lain telah membanjiri indonesia dgn kebijakan jokowi Bebas visa buat China";
# kalimat = "owi sepertinya kebijakan bebas visa bagi Cina lebih banyak merugikan Indonesia. Mgkn sudah saatnya Anda mencabut kebijakan tsb pic.twitter.com/klIQvP2jZj";
# kalimat = "administrasi tidak membangun administrasi dengan baik";
# kalimat = "@jokowi mendukung segala kebijakan bpk presiden krn sy percaya bpk akan memberikan yg terbaik bagi bangsa ini... Gbu"
# kalimat = "Jokowi Menilai Kebijakan AS Mementingkan Perekonomiannya Sendiri http:// dlvr.it/Mq6wGD";
# kalimat = "administrasi tidak ambruk dengan baik";
kalimat = "bukan indonesia yang melindungi";
print "Kalimat      : ";
print kalimat;
keyword = preprocessing.do(kalimat);
print "Preprocessing: ";
print keyword;
print "Klasifikasi kata: ";
hasil = role.play(keyword);
print hasil['counted'];
print hasil['score'];
# roleGroup = json.dumps(hasil['roleGroup']);
# print str(roleGroup);
print "Hasil Sentimen : "+str(hasil['sentiment']);

# naiveBayes.initial();
# print naiveBayes.play(keyword);

# old_tweet = open('data/old_tweets.csv','r');
# api = tweepy.API(auth);
# i = 0;
# for x in old_tweet:
#     if i > 17245:
#         p = x.split(';');
#         data = {};
#         content     = p[4];
#         data['content'] = content.replace("'","").replace('"','');
#         data['time']    = p[1];
#         try:
#             data['location']= api.get_user(p[0]).location.encode('cp1252').replace("'","").replace('"','').replace('\\','');
#         except BaseException as e:
#             data['location'] = "";

#         data['sosmed']  = 1;
#         data['user']    = p[0];
#         keyword         = preprocessing.do(content);
#         data['sentiment'] = role.play(keyword);
#         key = "";
#         for k in keyword:
#             key = key+k+"||";
#         data['keyword'] = key;

#         db_mysql.insertOpini(data);
#     print i;        
#     i = i+1;

# sql = "SELECT * FROM opini_pilkada2";
# db_mysql.executeSql(sql);
# result = db_mysql.fetch('all');
# for x in result:
#     opini = x[2];
#     k = preprocessing.do(opini);
#     v = role.play(k);
#     key = "";
#     i = 0;
#     for word in k:
#         if (i==0):
#             key = word;
#         else:
#             key = key+";|;"+word
#         i = i+1;
#     sql = '''UPDATE opini_pilkada2 SET sentiment=%d, keyword="%s" WHERE id=%d''' % (v,key,x[0]);
#     db_mysql.executeSql(sql);
#     db_mysql.commit();
#     print str(v)+" :: "+opini;

# k = preprocessing.do("Menjadikan hak bagus baik");
# v = role.play(k);

# sql = ''' SELECT * FROM main_dict ''';
# db_mysql.executeSql(sql);
# words = db_mysql.fetch('all');
# for word in words:
#     idword = word[0];
#     typeword = word[2];
#     valword = word[3];
#     print str(idword)+" "+str(typeword)+" "+str(valword);
#     if (valword != None and typeword != None):
#         sql = ''' UPDATE mining_dict_en SET type="%s", value=%d WHERE id=%d ''' % (typeword,valword,idword);
#         print sql;
#         db_mysql.executeSql(sql);
#     elif (typeword != None):
#         sql = ''' UPDATE mining_dict_en SET type="%s" WHERE id=%d ''' % (typeword,idword);
#         print sql;
#         db_mysql.executeSql(sql);
#     elif (valword != None):
#         sql = ''' UPDATE mining_dict_en SET value=%d WHERE id=%d ''' % (valword,idword);
#         print sql;
#         db_mysql.executeSql(sql);
# db_mysql.commit();
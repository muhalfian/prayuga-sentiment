import tweepy
import json
import datetime;
import re;

import db_mysql
import preprocessing;
import role;

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
 
api = tweepy.API(auth)
# search_result = api.search(q='kebijakan pemerintah jokowi lang:id',since="2016-01-01");

# for status in search_result:
#      data = status._json;
#      #keyword = preprocessing.do(data['text'].encode('utf-8'));
#      pprint(data['created_at']);

c = tweepy.Cursor(api.search,
                       q='kebijakan pemerintah jokowi since:2016-01-01 until:2017-12-02',
                       include_entities=True).items()
for status in c:
     data = status._json;
     #keyword = preprocessing.do(data['text'].encode('utf-8'));
     pprint(data['created_at']);

# while True:
#     try:
        
#     except tweepy.TweepError:
#         time.sleep(60 * 15)
#         continue
#     except StopIteration:
#         break


# class MyListener(StreamListener):
 
#     def on_data(self, tweet):
#         try:
#         	if 'retweeted_status' not in tweet:
#         		self.dataInput(tweet);
#         		return True;
#         except BaseException as e:
#             print("Error on_data: %s" % str(e))
#         return True
 
#     def on_error(self, status):
#         print(status)
#         return True

#     def dataInput(self,tweet):
#     	data = json.loads(tweet);
#     	keyword    = preprocessing.do(data['text']);
#         #sentiment  = role.play(keyword);
#     	data_input = {
#     		"content"  : data['text'],
#     		"time"     : datetime.datetime.fromtimestamp(int(data['timestamp_ms'])/1000),
#     		"location" : data['user']['location'],
#     		"sosmed"   : 1,
#     		"user"     : data['user']['screen_name'],
#     		"keyword"  : keyword,
#     	};
#     	db_mysql.insertOpini(data_input);

# twitter_stream = Stream(auth, MyListener())
# twitter_stream.filter(track=["Ormas"])

# content = "Aku memahami dengan baik";
# print "kalimat  :",content;
# keyword = preprocessing.do(content);
# print "keyword  :",keyword;
# sentiment  = role.play(keyword);
# print "Sentiment:",sentiment;

# words = db_mysql.migrasi();
# for word in words:
#     senti = db_mysql.checkSentimentalWord(word[1]);
#     if senti != None:
#         db_mysql.updateMigrasi(word[0], senti[3]);
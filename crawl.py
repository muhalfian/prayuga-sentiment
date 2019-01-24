import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import needed.db_mysql as db_mysql
import helper.preprocessing as preprocessing
import analyzer.impress as impress
import crawler.online_news.settings as settings;
from datetime import datetime 

import crawler.twitter.twitter as cr_twitter
from crawler.online_news.detikcom import DetikCom;
from crawler.online_news.liputan6 import Liputan6;
from scrapy.crawler import CrawlerProcess

def play():
	process_scrapy = CrawlerProcess({'USER_AGENT': settings.USER_AGENT})
	sql = 'SELECT * FROM apps_run WHERE status=1';
	db_mysql.executeSql(sql);
	appsRun = db_mysql.fetch('all');

	for app in appsRun:
		idApps   = app[1];
		idSosmed = app[2];

		sql = 'SELECT * FROM apps WHERE id='+str(idApps);
		db_mysql.executeSql(sql);
		apps = db_mysql.fetch('one');
		query = {};
		query['idApps'] = apps[0];
		query['qTwitter'] = apps[2];
		query['since']  = apps[6];
		query['until']  = apps[7];
		query['tags']   = apps[8].split(', ');
		query['q']      = apps[9];
		query['tags'].append(query['q']);
		print idSosmed;
		if(idSosmed == 1):
			dataTwitter = cr_twitter.play(query['qTwitter'],query['since'],query['until']);
			takeTwitter(idApps,dataTwitter);
		
		elif(idSosmed == settings.online_news['liputan6']):
			urls = [];
			if(query['until'] == None):
				query['until'] = datetime.today().strftime('%Y-%m-%d')
			for tag in query['tags']:
				tag = tag.replace(" ","-");
				urls.append('http://m.liputan6.com/tag/'+tag);
			process_scrapy.crawl(Liputan6,urls=urls,query=query)

		# Liputan6
		elif(idSosmed == settings.online_news['detikcom']):
			urls = [];
			q = query['q'].replace(" ","+");
			if(query['until'] == None):
				query['until'] = datetime.today().strftime('%Y-%m-%d')
			since = datetime.strptime(query['since'], "%Y-%m-%d").strftime("%d/%m/%Y");
			until = datetime.strptime(query['until'], "%Y-%m-%d").strftime("%d/%m/%Y");
			urls.append('https://www.detik.com/search/searchall?query='+q+'&sortby=time&fromdatex='+since+'&todatex='+until);
			process_scrapy.crawl(DetikCom,urls=urls,query=query)

	# print "=================================================process================================";
	process_scrapy.start() # the script will block here until the crawling is finished


def takeTwitter(idApps,data):
	for tweet in data:
		tweetContent 	   = db_mysql.escapeString(tweet.text.decode('utf-8'));
		tweetDate 		   = tweet.date;
		tweetId 		   = tweet.id;
		tweetRetweetCount  = tweet.retweets;
		tweetFacoriteCount = tweet.favorites;
		tweetHashtags      = tweet.hashtags;
		tweetMentions      = tweet.mentions;
		tweetUser          = tweet.username;
		tweetUserLocation  = tweet.geo;
	
		if(checkExist(tweetId,"twitter")):
			print tweetContent;
			dataProcess    = mainProcess(tweetContent,idApps);
			sentiment      = dataProcess['sentiment'];

			# for view counting rule impressi
			recordCounting = preprocessing.recordCounting(dataProcess);
			arr_word       = recordCounting['arr_word'];
			arr_counted    = recordCounting['arr_counted'];
			arr_score      = recordCounting['arr_score'];
			role_group     = recordCounting['role_group'];

			print tweetUser;
			print "::"+str(sentiment);
			sql = '''INSERT INTO apps_opinion(id_apps, sentiment, content, time, sosmed, tweet_id, tweet_retweet_count, tweet_favorite_count, tweet_hashtags, tweet_mentions, user, tweet_user_location, arr_word, arr_counted, arr_score, role_group) 
						VALUES ('%d','%s','%s','%s','%d','%s','%d','%d','%s','%s','%s','%s','%s','%s','%s','%s')''' \
						% (idApps, sentiment, str(tweetContent), tweetDate, 1, tweetId, tweetRetweetCount, tweetFacoriteCount, tweetHashtags, tweetMentions, str(tweetUser), tweetUserLocation, arr_word, arr_counted, arr_score, role_group);
			db_mysql.executeSql(sql);
			db_mysql.commit();

def checkExist(id, sosmed):
	if(sosmed == "twitter"):
		sql = 'SELECT * FROM apps_opinion WHERE tweet_id="'+str(id)+'"';
	db_mysql.executeSql(sql);
	data = db_mysql.fetch('one');
	if(data == None):
		return True;
	return False;

def mainProcess(text,idApps):
	keyword = preprocessing.do(text);
	result  = impress.play(keyword,idApps);
	return result;

play();
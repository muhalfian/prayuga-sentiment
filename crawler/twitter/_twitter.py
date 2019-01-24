import tweepy
import json
import datetime;
import re;
import time;

import needed.db_mysql as db_mysql

from tweepy import Stream
from tweepy.streaming import StreamListener
from pprint import pprint
from tweepy import OAuthHandler

consumer_key    = '30KgZnTiKCOYx8oPvlKeTyGJU';
consumer_secret = '43IHxBzgaVIB3bP95ORS2wfpQxs10R7fWsTU1FftVH7WQeMFMj';
access_token    = '595044868-NaibzrBxR7kCUZm9Qgosh6DCVnnOjaHZSest4eRb';
access_secret   = 'A1hPGJ1fIV4r8zLNMdapaaXQDG5OlI5L8u04rUtrqMMSF';

auth = OAuthHandler(consumer_key, consumer_secret);
auth.set_access_token(access_token, access_secret);
api = tweepy.API(auth);

def play(query):
	c = tweepy.Cursor(api.search,
                       q=query,
                       show_user=True).items()
	# i = 1;
	# for status in c:
	#      data = status._json;
	#      print str(i)+") "+data['created_at'];
	#      i = i+1;
	i = 1;
	while True:
		try:
			tweet = c.next();
			data = tweet._json;
			print str(i)+") "+data['created_at'];
			i = i+1;
		except tweepy.TweepError:
			time.sleep(60 * 15)
			continue
		except StopIteration:
			break
	     
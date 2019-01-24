import datetime
import got
import needed.db_mysql as db_mysql

def play(query,since,until=None):
	
	def printTweet(descr, t):
		print descr
		print "ID: %s" % t.id
		print "Date: %s" % t.date
		print "Name: %s" % t.name
		print "Username: %s" % t.username
		print "Retweets: %d" % t.retweets
		print "Favorites: %d" % t.favorites
		print "Text: %s" % t.text
		print "Mentions: %s" % t.mentions
		print "Hashtags: %s" % t.hashtags
		print "Geo: %s\n" % t.geo
	
	
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(since);
	if(until == None):
		until = str(datetime.date.today() + datetime.timedelta(days=1));
	tweetCriteria = tweetCriteria.setUntil(until);
	# tweetCriteria = tweetCriteria.setMaxTweets(16);
	tweets = got.manager.TweetManager.getTweets(tweetCriteria);

	return tweets;
	
	# Example 3 - Get tweets by username and bound dates
	# tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil("2015-09-12").setMaxTweets(1)
	# tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	
	# printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']", tweet)

# if __name__ == '__main__':
# 	play()
	
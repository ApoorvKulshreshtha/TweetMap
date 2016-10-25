from elasticsearch import Elasticsearch, RequestsHttpConnection
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import sys, traceback

es = Elasticsearch( [{'host':'search-tweet-c3mkhiza33cstn5qrvotrsw7my.us-west-2.es.amazonaws.com', 'port':443,'use_ssl':True}])

ckey = ''
csecret =''
atoken = ''
asecret = ''

class StreamListener(StreamListener):
	def on_data(self, data):
		if(data == None):
			return 
		if not data.coordinates:
			return 
		try:
			StreamedData = json.loads(data)
		except:
			return 
		try:
			StreamedTweet={}
			print StreamedData['id']
			StreamedTweet['id'] = StreamedData['id']
			StreamedTweet['text'] = StreamedData['text']
			StreamedTweet['coordinates'] = StreamedData['coordinates']
			StreamedTweet['retweet-count'] = StreamedData['retweet-count']
			StreamedTweet['favorite-count'] = StreamedData['favorite-count']
			StreamedTweet['user-name'] = StreamedData['user-name']
			StreamedTweet['hashtag'] = [hashtags['text'] for hashtags in StreamedData['entities']['hashtags']]
			if(StreamedData['coordinates']):
				es.index(index = 'twitter_feed', doc_type = 'tweets', id = StreamedTweet['id'], body = StreamedTweet)
		except Exception as e:
			pass
		time.sleep(0.1)
		return True

	def on_error(self, status):
		if(status == 420):
			time.sleep(1)

if __name__ == '__main__':
	auth = OAuthHandler(ckey, csecret)
	auth.set_access_token(atoken, asecret)
	twitterStream = Stream(auth, StreamListener())
	while True:
		try:
			twitterStream.filter(locations=[-180,-90,180,90])
		except Exception as e:
			pass

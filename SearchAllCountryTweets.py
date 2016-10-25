from elasticsearch import Elasticsearch
import tweepy
import time

# Retrieve tweet text, id, coordinates, user, user id, time, number of re-tweet, number of liked

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Authentication
api = tweepy.API(auth)
# Add location search to India
places = api.geo_search(query="India", granularity="country")
place_id = places[0].id

es = Elasticsearch([{'host': 'search-tweet-c3mkhiza33cstn5qrvotrsw7my.us-west-2.es.amazonaws.com', 'port': 443, 'use_ssl': True}])


while True:
        data = api.search(q="place:%s" % place_id, count = 100)
        for singleTweet in data:
                if not singleTweet.coordinates:
                        continue
                tweeter = {}
                tweeter['id'] = singleTweet.id
                tweeter['text'] = singleTweet.text
                tweeter['user-name'] = singleTweet.user.name
                tweeter['user-id'] = singleTweet.user.id
                tweeter['hashtag'] = [hashtag['text'] for hashtag in singleTweet.entities['hashtags']]
                tweeter['coordinates'] = singleTweet.coordinates['coordinates']
                tweeter['place'] = ''
                if singleTweet.place:
                        tweeter['place'] = singleTweet.place.full_name
                tweeter['created-at'] = ''
                if singleTweet.created_at:
                        tweeter['created-at'] = singleTweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
                tweeter['retweet-count'] = singleTweet.retweet_count
                tweeter['favorite-count'] = singleTweet.favorite_count
                #print (data.text)
                es.index(index = 'twitter', doc_type = 'tweets', id = singleTweet.id, body = tweeter)
                print("found a geolocated tweet at ", tweeter['coordinates'])

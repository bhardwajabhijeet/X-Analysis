import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient

api_key = "nZFOfrTPwZlVW0N089axoYYVZ"
api_secret_key = "xtutntqz2HOusNkVDUxk7ToyBPXjtQX5qeZFnBf6QMQvw2K8U8"
access_token = "1232330306671304715-CrHuxQp4XdWj5abD9IxqI4nkblTP1s"
access_secret_token = "qbjWM5FVynFo23U5BKO6DQU2cR3fYzjERK31tKCnRlOzc"

connect = MongoClient()

db = connect.tweetsData

collection = db.tweets

class TwitterStreamer():
	def stream_tweets(self, tweets_filename, keywords_list):
		listener = TwitterListener(tweets_filename)
		auth = OAuthHandler(api_key, api_secret_key)
		auth.set_access_token(access_token, access_secret_token)

		stream = Stream(auth, listener, tweet_mode = 'extended')

		stream.filter(track = keywords_list)

class TwitterListener(StreamListener):

	def __init__(self, tweets_filename):
		self.tweets_filename = tweets_filename
		self.max_tweets = 100
		self.tweet_count = 0

	def on_data(self, data):
		try:
			if self.max_tweets == self.tweet_count:
				print("Completed")
				return False
			else:
				self.tweet_count+=1
				print(data)
				collection.insert_one(json.loads(data))
				print(self.tweet_count)
				with open(self.tweets_filename, 'a') as tf:
					tf.write(data)
					tf.write(',')
				
		except BaseException as e:
			print("Error on_data: " + str(e))
			return True

	def on_error(self,status):
		print(status)


if __name__ == "__main__":
	
	keywords_list = ['Canada', 'University', 'Halifax', 'Canada Education', 'Dalhousie University']
	tweets_filename = "tweets.json"
	auth = OAuthHandler(api_key, api_secret_key)
	auth.set_access_token(access_token, access_secret_token)
	api = tweepy.API(auth)
	
	for keyword in keywords_list:
		with open(tweets_filename, "a") as tf:
			list = [keyword]
			print(list)
			for tweet in tweepy.Cursor(api.search, q=keyword, lang='en', tweet_mode = 'extended').items(550):
				j = json.dumps(tweet._json)
				print(j)
				collection.insert_one(json.loads(j))
				tf.write(j)
				tf.write(',')

			print("StreamListener Active for " + keyword)
			twitter_streamer = TwitterStreamer()
			twitter_streamer.stream_tweets(tweets_filename, list)	

cursor = collection.find()
for record in cursor:
	print(record)
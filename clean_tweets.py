import re
import json
from pymongo import MongoClient

connect = MongoClient()
db = connect.tweetsData
collection = db.tweets
clean_collection = db.cleanTweets

for record in collection.find():
	tweet_text = record['full_text']
	#following regex removes emojis and othe special characters
	emoji_pattern = re.compile("["	
						u"\U0001F600-\U0001F64F"
		               	u"\U0001F300-\U0001F5FF"  
       	            	u"\U0001F680-\U0001F6FF"  
           	        	u"\U0001F1E0-\U0001F1FF"  
               	    	u"\U00002702-\U000027B0"
                   		u"\U000024C2-\U0001F251"
                   		"]+", flags=re.UNICODE)
	tweet_text = emoji_pattern.sub(r'', tweet_text)
	tweet_text = re.sub('http\S+',' ',tweet_text)
	tweet_text = re.sub('[^0-9a-zA-Z\ ]+',' ',tweet_text)
	clean_record = record
	clean_record['full_text'] = tweet_text
	clean_collection.insert_one(clean_record)


clean_collection = db.cleanTweets
cursor = clean_collection.find()
counter = 1

with open('clean_tweets_data.txt', 'a') as d:
	for record in cursor:
		d.write(record['full_text'].lower())
		d.write(" ")

with open('clean_tweets_data.txt', 'a') as d:
	for record in cursor:
		counter += 1
		max_tweets = cursor.count()
		record.pop('_id', None)
		if max_tweets == 1:
			d.write(json.dumps(record))
		elif max_tweets >= 1 and counter <= max_tweets - 1:
			d.write(json.dumps(record))
			d.write(',')
		elif counter == max_tweets:
			d.write(json.dumps(record))
		d.write(']')

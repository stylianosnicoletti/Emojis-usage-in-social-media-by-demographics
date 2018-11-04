import json
import pandas as pd

# Path of tweets sample
tweets_data_path = '/home/stelios/Desktop/Honours Project/Samples/tweets_sample.txt'

# Path of emojis json
emojis_json_data_path = 'emojis.json'

# Open tweets sample
tweets_file = open(tweets_data_path, "r")

# To store sample data with attributes needed
# https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object.html
data = {'created_at':[],
'tweet_id':[],
'source_device': [],
'in_reply_to_status_id':[],
'in_reply_to_user_id':[],
'text_tweet': [],
'lang': [],
'country': [],
'user_id':[],
'user_name':[],
'followers_count':[],
'friends_count':[],
'statuses_count':[],
'user_favourites_count':[],
'prof_picture': [],
'quote_count':[],
'reply_count':[],
'retweet_count':[],
'favorite_count':[],
'entities_hashtags':[],
'entities_user_mentions':[]}

# An empty list to store emojis
emojis_list =[]

# Function: Json of emojis to list (1640 emojis) 
def fill_emojis_list(list,emojis_json):
	with open(emojis_json) as f:
		data = json.load(f)

	for element in data:
		list.append(element['emoji'])
	print(len(list))				

# Function: Create list with the attributes needed and with tweets that have emojis 
def fill_sample_including_emojis(data_attributes,file,emojis_list):
	for line in file:
		try:
			tweet = json.loads(line)
			# If there is an emoji in tweet 
			if any(emoji in tweet['text'] for emoji in emojis_list):
				data_attributes['created_at'].append(tweet['created_at'])
				data_attributes['tweet_id'].append(tweet['id'])
				data_attributes['source_device'].append(tweet['source']if tweet['source'] != None else None)
				data_attributes['in_reply_to_status_id'].append(tweet['in_reply_to_status_id']if tweet['in_reply_to_status_id'] != None else None)
				data_attributes['in_reply_to_user_id'].append(tweet['in_reply_to_user_id']if tweet['in_reply_to_user_id'] != None else None)
				data_attributes['text_tweet'].append(tweet['text'])
				data_attributes['lang'].append(tweet['lang'])
				data_attributes['country'].append(tweet['place']['country']if tweet['place'] != None else None)
				data_attributes['user_id'].append(tweet['user']['id']if tweet['user']['id'] != None else None )
				data_attributes['user_name'].append(tweet['user']['name'])
				data_attributes['followers_count'].append(tweet['user']['followers_count']if tweet['user']['followers_count'] != None else None)
				data_attributes['friends_count'].append(tweet['user']['friends_count']if tweet['user']['friends_count'] != None else None)
				data_attributes['statuses_count'].append(tweet['user']['statuses_count']if tweet['user']['statuses_count'] != None else None)
				data_attributes['user_favourites_count'].append(tweet['user']['favourites_count']if tweet['user']['favourites_count'] != None else None)
				# Trim size normal from picture url so as to display original size profile picture
				data_attributes['prof_picture'].append("{}{}".format(tweet['user']['profile_image_url_https'][:-11],".jpg"))
				data_attributes['quote_count'].append(tweet['quote_count']if tweet['quote_count'] != None else None)
				data_attributes['reply_count'].append(tweet['reply_count']if tweet['reply_count'] != None else None)
				data_attributes['retweet_count'].append(tweet['retweet_count']if tweet['retweet_count'] != None else None)
				data_attributes['favorite_count'].append(tweet['favorite_count']if tweet['favorite_count'] != None else None)
				data_attributes['entities_hashtags'].append(tweet['entities']['hashtags']if tweet['entities']['hashtags'] != None else None)
				data_attributes['entities_user_mentions'].append(tweet['entities']['user_mentions']if tweet['entities']['user_mentions'] != None else None)
		except:
			continue


# Fill the list of 1640 emojis
fill_emojis_list(emojis_list,emojis_json_data_path)

# Fill list with tweets that inlude emojis
fill_sample_including_emojis(data,tweets_file,emojis_list)

# Create panda dataframe with tweets including emojis
tweets_with_emojis_df = pd.DataFrame(data)

# Extract to dataframe to json
tweets_with_emojis_df.to_json('tweets_sample_with_emojis.json')


print(tweets_with_emojis_df)



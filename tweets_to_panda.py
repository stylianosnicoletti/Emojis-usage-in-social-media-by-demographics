import json
import pandas as pd


tweets_data_path = 'twitter_data.txt'

tweets_data = []
tweets_file = open(tweets_data_path, "r")

data = {'text': [], 'lang': [], 'country': [], 'prof_picture': []}

# An empty list to store emojis
emojis_list =[]

# Json of emojis to list
def fill_emojis_list(list,emojis_json):
	with open(emojis_json) as f:
		data = json.load(f)

	for element in data:
		print element['name']
		print repr(element['emoji'])
		print element['emoji']
		list.append(element['emoji'])
		print(len(list))				# 1640 emojis 


#tweets = pd.DataFrame(data)

for line in tweets_file:
	try:
		tweet = json.loads(line)
		tweets_data.append(tweet)
		data['text'].append(tweet['text'])
		data['lang'].append(tweet['lang'])
		data['country'].append(tweet['place']['country']if tweet['place'] != None else None)
		# Trim size normal from picture url so as to display original size profile picture
		data['prof_picture'].append("{}{}".format(tweet['user']['profile_image_url_https'][:-11],".jpg"))
	except:
		continue

#print len(tweets_data)
tweets = pd.DataFrame(data)
#pd.set_option('display.max_colwidth',1000)
#print tweets
#print str(tweets['prof_picture'])


	# Fill the list of 1640 emojis
	#fill_emojis_list(emojis_list,'emojis.json')

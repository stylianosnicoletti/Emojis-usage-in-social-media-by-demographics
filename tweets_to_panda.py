import json
import pandas as pd

# Path of tweets sample
tweets_data_path = 'tweets_sample.txt'

# Open tweets sample
tweets_file = open(tweets_data_path, "r")

# To store sample data with attributes needed
data = {'text': [], 'lang': [], 'country': [], 'prof_picture': []}

# An empty list to store emojis
emojis_list =[]

# Function: Json of emojis to list (1640 emojis) 
def fill_emojis_list(list,emojis_json):
	with open(emojis_json) as f:
		data = json.load(f)

	for element in data:
		print element['name']
		print repr(element['emoji'])
		print element['emoji']
		list.append(element['emoji'])
		print(len(list))				

# Function: Create a panda dataframe with the attributes needed
def sample_to_panda_dataframe(data_attributes,file):
	for line in file:
		try:
			tweet = json.loads(line)
			data_attributes['text'].append(tweet['text'])
			data_attributes['lang'].append(tweet['lang'])
			data_attributes['country'].append(tweet['place']['country']if tweet['place'] != None else None)
			# Trim size normal from picture url so as to display original size profile picture
			data_attributes['prof_picture'].append("{}{}".format(tweet['user']['profile_image_url_https'][:-11],".jpg"))
		except:
			continue
	tweets = pd.DataFrame(data_attributes)
	print tweets

sample_to_panda_dataframe(data,tweets_file)



	# Fill the list of 1640 emojis
	#fill_emojis_list(emojis_list,'emojis.json')

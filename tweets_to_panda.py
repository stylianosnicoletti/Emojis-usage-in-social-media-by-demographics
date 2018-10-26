import json
import pandas as pd

# Path of tweets sample
tweets_data_path = 'tweets_sample.txt'

# Path of emojis json
emojis_json_data_path = 'emojis.json'

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
		#print element['name']
		#print repr(element['emoji'])
		#print element['emoji']
		list.append(element['emoji'])
	print(len(list))				

# Function: Create list with the attributes needed and with tweets that have emojis 
def sample_to_including_emojis(data_attributes,file,emojis_list):
	for line in file:
		try:
			tweet = json.loads(line)
			# If there is an emoji in tweet 
			if any(emoji in tweet['text'] for emoji in emojis_list):
				data_attributes['text'].append(tweet['text'])
				data_attributes['lang'].append(tweet['lang'])
				data_attributes['country'].append(tweet['place']['country']if tweet['place'] != None else None)
				# Trim size normal from picture url so as to display original size profile picture
				data_attributes['prof_picture'].append("{}{}".format(tweet['user']['profile_image_url_https'][:-11],".jpg"))
		except:
			continue


# Fill the list of 1640 emojis
fill_emojis_list(emojis_list,emojis_json_data_path)
#print(emojis_list)

# Fill list with tweets that inlude emojis
sample_to_including_emojis(data,tweets_file,emojis_list)

# Create panda dataframe with tweets including emojis
tweets_with_emojis_df = pd.DataFrame(data)

# Extract to dataframe to json
tweets_with_emojis_df.to_json('tweets_sample_with_emojis.json')


print(tweets_with_emojis_df)



import json
import pandas as pd

# Path of tweets sample
tweets_with_emojis_data_path = 'tweets_sample_with_emojis.json'

# Path of emojis json
emojis_json_data_path = 'emojis.json'

# From json to panda 
tweets_with_emojis_df = pd.read_json(tweets_with_emojis_data_path)

# For each emoji print its counts 
with open(emojis_json_data_path) as f:
	data = json.load(f)

	for element in data:
		emoji_counter = 0 
		for tweet in tweets_with_emojis_df['text']:
			if element['emoji'] in tweet:
				emoji_counter = emoji_counter + 1
		print ("Emoji: {}\n Counts: {}\n".format(element['name'],emoji_counter))
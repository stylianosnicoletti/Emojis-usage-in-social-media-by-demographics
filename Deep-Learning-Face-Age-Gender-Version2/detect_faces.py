# USAGE
# python detect_faces.py --confidence 0.98

# import the necessary packages
import numpy as np
import argparse
import cv2
import pandas as pd
from skimage import io

# Path of tweets sample
tweets_with_emojis_data_path = '/home/stelios/Desktop/Honours Project/Emojis-usage-in-social-media-by-demographics/Streaming-Emojis-Capture/tweets_sample_with_emojis.json'

# From json to panda 
tweets_with_emojis_df = pd.read_json(tweets_with_emojis_data_path)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
gender_list = ['Female', 'Male']

# load our serialized model from disk
print("[INFO] loading models...")

def initialize_caffe_models():

	# https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/
	face_net = cv2.dnn.readNetFromCaffe(
		'/home/stelios/Desktop/Honours Project/Models/deploy.prototxt',
		'/home/stelios/Desktop/Honours Project/Models/res10_300x300_ssd_iter_140000.caffemodel')
	
	# https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/
	age_net = cv2.dnn.readNetFromCaffe(
		'/home/stelios/Desktop/Honours Project/Models/dex_imdb_wiki.prototxt', 
		'/home/stelios/Desktop/Honours Project/Models/dex_imdb_wiki.caffemodel')

	# https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/
	gender_net = cv2.dnn.readNetFromCaffe(
		'/home/stelios/Desktop/Honours Project/Models/gender.prototxt', 
		'/home/stelios/Desktop/Honours Project/Models/gender.caffemodel')
		
	return(face_net,age_net, gender_net)
	
face_net, age_net, gender_net = initialize_caffe_models()

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
for ind,prof in enumerate(tweets_with_emojis_df['prof_picture']):

	# To temporalily store faces with confidence higher than arg confidence
	temp_faces_age_gender = {'age':[],'gender':[]}

	try:
		image = io.imread(tweets_with_emojis_df['prof_picture'][ind])
		(h, w) = image.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 3,
			(300, 300), (104.0, 177.0, 123.0))

		# pass the blob through the network and obtain the detections and
		# predictions
		##print("[INFO] computing object detections...")
		face_net.setInput(blob)
		detections = face_net.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with the
			# prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence > args["confidence"]:

				# compute the (x, y)-coordinates of the bounding box for the
				# object
			##	print(confidence)
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				
				# Get Face 
				face_img = image[startY:endY, startX:endX].copy()
				blob_face = cv2.dnn.blobFromImage(cv2.resize(face_img, (224, 224)), 3,
			(224, 224), (104.0, 177.0, 123.0))
				#cv2.imshow("Output", face_img)
				
				#Predict Gender
				gender_net.setInput(blob_face)
				gender_preds = gender_net.forward()
				gender = gender_list[gender_preds[0].argmax()]
			##	print("Gender : " + gender)

				# Append gender to temp list
				temp_faces_age_gender['gender'].append(gender)
				
				#Predict Age
				age_net.setInput(blob_face)
				age_preds = age_net.forward()
				# 101 neurons 0-100 
				age = str(age_preds[0].argmax())
			##	print("Age : " + age)

				# Append age to to temp list
				temp_faces_age_gender['age'].append(age)
		 
				# draw the bounding box of the face along with the associated
				# age and gender 
				text = "{} {}".format(gender,age)
				y = startY - 10 if startY - 10 > 10 else startY + 10
				cv2.rectangle(image, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
				cv2.putText(image, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		
		cv2.imshow("Output", image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	except:
		pass
	# If one face/age/gender etsimation found, update panda dataframe 
	if ((len(temp_faces_age_gender['age'])==1) & (len(temp_faces_age_gender['gender'])==1)):
		tweets_with_emojis_df.at[ind, 'est_age'] = temp_faces_age_gender['age'][0]
		tweets_with_emojis_df.at[ind,'est_gender'] = temp_faces_age_gender['gender'][0]

# Extract to dataframe to json
tweets_with_emojis_df.to_json('tweets_sample_with_emojis_ages_genders.json')
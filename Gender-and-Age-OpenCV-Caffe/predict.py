import cv2
import imutils
import time
import numpy as np
import pandas as pd
from skimage import io

# Path of tweets sample
tweets_with_emojis_data_path = '../tweets_sample_with_emojis.json'

# From json to panda 
tweets_with_emojis_df = pd.read_json(tweets_with_emojis_data_path)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
gender_list = ['Male', 'Female']

def initialize_caffe_models():
	
	age_net = cv2.dnn.readNetFromCaffe(
		'data/deploy_age.prototxt', 
		'data/age_net.caffemodel')

	gender_net = cv2.dnn.readNetFromCaffe(
		'data/deploy_gender.prototxt', 
		'data/gender_net.caffemodel')

	return(age_net, gender_net)

def read_from_camera(age_net, gender_net):
	font = cv2.FONT_HERSHEY_SIMPLEX

	for prof in tweets_with_emojis_df['prof_picture']:
		try:
			image = io.imread(prof)
				
			face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')
			
			gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			faces = face_cascade.detectMultiScale(gray,scaleFactor=1.1, minNeighbors=5)

			if(len(faces)>0):
				print("Found {} faces".format(str(len(faces))))
			else:
				print("Not found")

			for (x, y, w, h )in faces:
				cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)

				# Get Face 
				face_img = image[y:y+h, h:h+w].copy()
				blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

				#Predict Gender
				gender_net.setInput(blob)
				gender_preds = gender_net.forward()
				gender = gender_list[gender_preds[0].argmax()]
				print("Gender : " + gender)

				#Predict Age
				age_net.setInput(blob)
				age_preds = age_net.forward()
				age = age_list[age_preds[0].argmax()]
				print("Age Range: " + age)

				overlay_text = "%s %s" % (gender, age)
				cv2.putText(image, overlay_text, (x, y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)


			cv2.imshow('image',image)
		#cv2.waitKey(0)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		except:
			pass

if __name__ == "__main__":
	age_net, gender_net = initialize_caffe_models()

	read_from_camera(age_net, gender_net)





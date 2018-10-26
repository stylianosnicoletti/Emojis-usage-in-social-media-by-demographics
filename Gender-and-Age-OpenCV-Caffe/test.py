# import the necessary packages
import numpy as np
import urllib
import cv2
# METHOD #2: scikit-image
from skimage import io
 
# initialize the list of image URLs to download
urls = [
	"https://www.pyimagesearch.com/wp-content/uploads/2015/01/opencv_logo.png",
	"https://www.pyimagesearch.com/wp-content/uploads/2015/01/google_logo.png",
	"https://www.pyimagesearch.com/wp-content/uploads/2014/12/adrian_face_detection_sidebar.png",
]

# loop over the image URLs
for url in urls:
	# download the image using scikit-image
	print "downloading %s" % (url)
	image = io.imread(url)
	cv2.imshow("Incorrect", image)
	cv2.imshow("Correct", cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
	cv2.waitKey(0)

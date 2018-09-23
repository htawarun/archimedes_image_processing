# This code will quantify blurriness in multiple images. 
# In return, it will find prescense of Astigmatism in the optics system. 
# Code developed by Kay Lee of Illumina. 

# import packages necessary
import cv2
from imutils import paths
import argparse


# compute the Laplacian of the image and return the focus
# the "measure" is simply the variance of the Laplacian
def variance_of_laplacian(image):
	return cv2.Laplacian(image, cv2.CV_64F).var()

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", 
	required=True,
	help="path to input directory of images")
ap.add_argument("-t","--threshold", 
	type=float,
	default=100.00,
	help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

# loop over the input images
for imagePath in paths.list_images(args["images"]):
	# load the image
	image = cv2.imread(imagePath)
	# convert into grayscale
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	# focus measure of the image using VAR of Laplacian
	fm = variance_of_laplacian(gray)
	text = "No Astigmatism"

	# if the focus measure is lower than the threshold, image is considered "blurry"
	if fm < args["threshold"]:
		text = "Astigmatism"

# show image and computed measure results
	cv2.putText(image, "{}: {:.2f}".format(text, fm), (20,50),
		cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
	
	cv2.imshow("Image", image)
	key = cv2.waitKey(10)
	print "Astigmatism score is {:.5f}.".format(1/fm)





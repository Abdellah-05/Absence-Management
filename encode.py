# python encode_faces.py --dataset dataset --encodings encodings.pickle
from imutils import paths
import face_recognition
import argparse
import pickle
from cv2 import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True, help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings",  required=True, help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="cnn", help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())

# grab the paths to the input images in our dataset
imagePaths = list(paths.list_images(args["dataset"]))

# initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# extract the person name from the image path
	name = imagePath.split(os.path.sep)[-2]

	image = cv2.imread(imagePath)
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	#resize image to 1/2
	rgb_small = cv2.resize(rgb, (0, 0), fx=0.5, fy=0.5)

	boxes = face_recognition.face_locations(rgb,model=args["detection_method"])

	# encode image only if face locations were found
	if boxes != []:
		encodings = face_recognition.face_encodings(rgb, boxes)

		for encoding in encodings:
			knownEncodings.append(encoding)
			knownNames.append(name)
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
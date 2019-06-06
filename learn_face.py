from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

#Create a parser and collect the path to the face to be learned
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required=True, help="Path to the person's data set")
args = vars(parser.parse_args())

#Collect the paths to each image in the dataset
folder_path = args["path"]
image_paths = list(paths.list_images(folder_path))

#Deduce the name of the person from the data folder
name = folder_path[2:-5]  #./name_data

#Initialize list that will store the encodings for the training images
encodings = []

for image_path in image_paths:
    #Read the image from OpenCV and convert it to RGB color channels
    image = cv2.imread(image_path)
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #Detect the bounding boxes of faces in the image
    boxes = face_recognition.face_locations(rgb, model="hog")

    #Compute encoding for the faces in the image
    image_encodings = face_recognition.face_encodings(rgb, boxes)

    #Add encoding to list of known encodings for this person
    [encodings.append(encoding) for encoding in image_encodings]

#Creates the dictionary to be saved to the pickle file
data = {"encodings": encodings, "names": [name] * len(encodings)}
file_name = "./Encodings/" + name + "_encodings.pickle"
f = open(file_name, "wb")
f.write(pickle.dumps(data))
f.close()



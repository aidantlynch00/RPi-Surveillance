from picamera import PiCamera
from time import sleep
import argparse
import string

#Create argument parser to get the name of the person
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--name", required=True, help="Name of the person being added to the data set.")
args = vars(parser.parse_args())

name = args["name"]

#Create camera
camera = PiCamera()
camera.start_preview()
sleep(5)

#Capture photos to a unique data folder for the person
folder = "./" + name + "_data"
for i in range(30):
    filename = name + str(i) + ".jpeg"
    camera.capture(folder + filename)
    sleep(2)

#Release camera resources
camera.stop_preview()
camera.close()

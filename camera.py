from picamera import PiCamera
from time import sleep
from PIL import Image
from io import BytesIO
import numpy as np

def variance(frame1, frame2):
    img_width, img_height = frame1.size()
    
    variance_sums = [3]

    #For each pixel
    for x in range(img_width):
        for y in range(img_height):
            #Fetch the RGB values of each image at the pixel (x, y)
            rgb1 = frame1.getpixel((x, y))
            rgb2 = frame2.getpixel((x, y))

            #Difference in each channel represented as a number between 0 and 1
            r_variance = abs(rgb1[0] - rgb2[0]) / 255
            g_variance = abs(rgb1[1] - rgb2[1]) / 255
            b_variance = abs(rgb1[2] - rgb2[2]) / 255

            #Add to the overall variance in the image
            variance_sums[0] += r_variance
            variance_sums[1] += g_variance
            variance_sums[2] += b_variance

    num_pixels = img_width * img_height

    #Take the average variance of each channel over the entire image
    variance_sums[0] /= num_pixels
    variance_sums[1] /= num_pixels
    variance_sums[2] /= num_pixels

    #Compute the overall variance score using each channel
    return (variance_sums[0] + variance_sums[1] + variance_sums[2]) / 3


###MAIN###

#Create a PiCamera object
camera = PiCamera()
camera.led = False

#Declare bit stream and image variables
stream = BytesIO()
prev_frame = None
curr_frame = None

#Assign variance threshold
threshold = .13 #TODO: change arbitrary number lol

#Main camera loop
while True:
    prev_frame = curr_frame

    #Capture image to bit stream
    camera.capture(stream, format = 'jpeg')
    stream.seek(0) #Reset pointer to start of stream to read data

    curr_frame = Image.open(stream)

    #Compute variance between frames
    if prev_frame != None and curr_frame != None:
        variance = variance(prev_frame, curr_frame)
        print('Variance: ' + variance)

        #If the variance is greater than set threshold, pass curr_frame into OpenCV
        if variance > threshold:
            #Run OpenCV algorithm
            pass
    sleep(5)

    

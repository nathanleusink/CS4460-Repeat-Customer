###
# Title: customer_reaction.py
# Author: Nathan Leusink
# Class: CS 4460
# Description: The purpose of this code is to:
#               1. Recognize Someones Face
#               2. Detect the emotion on someones face
#               3. If the computer is at least 50% certain the emotion is correct
#                   i. If bad emotion, make negative change
#                   ii. If good emotion, reinforce positive change
#                   iii. If neutral emotion, nothing changes
###

#Import Statements
import cv2
import numpy as np
from PIL import Image, ImageOps
from keras import models
import os
import tensorflow as tf
import time

#Special Modules needed from keras for CNN
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

#Global Variable
frames = 0

def recognizeFace():
    ### Recognizing Someones Face ###
    
    global frames
    print("[LOG] Looking for faces ...")
    
    #Importing OpenCV Haar Cascade
    cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    # Init Camera
    video_capture = cv2.VideoCapture(0)
    
    #Facial Recognition
    face_found = False

    #Looking for face
    while face_found == False:

        #Getting Single Frame from Camera
        ret, frames = video_capture.read()

        #Converting to Grayscale
        gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)

        #Finding Faces using Haar Cascade
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        #Determining if a face has been found
        if(len(faces) > 0):
            face_found = True
            print("[EVENT] FACE FOUND")
        else:
            print("[EVENT] FACE NOT FOUND. CONTINUING TO LOOK")
            print("[LOG] Sleeping 15 Seconds")
            time.sleep(15)
            
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frames, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return face_found


def recognizeEmotion():
    
    ### Emotion Recognition ###

    global frames
    
    #Loading CNN For Emotional Recognition
    print("[LOG] Loading CNN Model... ")
    base_path = os.getcwd()
    model = keras.models.load_model(base_path + '\\cnn_result.h5')
    print("[LOG] CNN Model Loaded.")

    #Setting Input Size
    keras.layers.InputLayer(input_shape=(48, 48, 1))

    #Load Image --> Convert to Gray Scale --> Resize to 48 by 48 pixels
    print("[LOG] Formatting Input.")
    face_image = Image.fromarray(frames, 'RGB')
    face_image = ImageOps.grayscale(face_image)
    face_image = face_image.resize((48,48))

    #Converting Image to Numpy Array
    image_array = np.array(face_image)
    
    #Expanding Matching Tensor 4D Shape
    image_array = np.expand_dims(image_array, axis=0)

    #Making Prediction
    print("[LOG] Making Prediction")
    prediction = model.predict(image_array)

    return prediction

def decodePrediction(prediction):

    emotion_recognized = ""
    weighted_pso_change = 50
    
    confidence = np.amax(prediction)
    max_index = np.argmax(prediction)

    match max_index:

        #Angry
        case 0:
            emotion_recognized = "Angry"

        #Digust
        case 1:
            emotion_recognized = "Disgust"

        #Fear
        case 2:
            emotion_recognized = "Fear"

        #Happy
        case 3:
            emotion_recognized = "Happy"

        #Neutral
        case 4:
            emotion_recognized = "Neutral"

        #Sad
        case 5:
            emotion_recognized = "Sad"

        #Surpised
        case 6:
            emotion_recognized = "Surpised"
    
    print("Emotion: ", emotion_recognized, " Confidence: ", confidence*100,"%")

    #Setting confidence greater than 50% to enact change
    if(confidence > .50):

        if(emotion_recognized == "Sad" or emotion_recognized == "Angry" or emotion_recognized == "Disgust"):
            weighted_pso_change = 0

        elif(emotion_recognized == "Happy"):
            weighted_pso_change = 100

        else:
            weighted_pso_change = 50
    else:
        print("[LOG] Confidence level was below 50%. Discarding data")

    return weighted_pso_change

    
def external_control_loop():

    #Find Face
    face_found = recognizeFace()

    #Recognize Emotion
    if(face_found):
        prediction = recognizeEmotion()

        #Returning Change to PSO Algorithm
        weighted_pso_change = decodePrediction(prediction)

    return weighted_pso_change

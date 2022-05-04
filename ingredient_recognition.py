###
# Title: ingredient_recognition.py
# Author: Kristen Farmer
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


def recognize_ingredient():
    
    ### Ingredient Recognition ###

    # Init Camera
    video_capture = cv2.VideoCapture(0)
    
    
    #Getting Single Frame from Camera
    ret, frames = video_capture.read()

    #Converting to Grayscale
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    
    #Loading CNN For Ingredient Recognition *************** CHANGE THIS
    print("[LOG] Loading CNN Model... ")
    base_path = os.getcwd()
    model = keras.models.load_model(base_path + '\\cnn_result.h5')
    print("[LOG] CNN Model Loaded.")

    #Setting Input Size ******* CHANGE THIS
    keras.layers.InputLayer(input_shape=(48, 48, 1))

    #Load Image --> Convert to Gray Scale --> Resize to 48 by 48 pixels ********* size
    print("[LOG] Formatting Input.")
    ingredient_image = Image.fromarray(frames, 'RGB')
    ingredient_image = ImageOps.grayscale(ingredient_image)
    ingredient_image = ingredient_image.resize((48,48))

    #Converting Image to Numpy Array
    image_array = np.array(ingredient_image)
    
    #Expanding Matching Tensor 4D Shape
    image_array = np.expand_dims(image_array, axis=0)

    #Making Prediction
    print("[LOG] Making Prediction")
    prediction = model.predict(image_array)

    return prediction

def decodePrediction(prediction):

    ingredient_recognized = ""
    
    confidence = np.amax(prediction)
    max_index = np.argmax(prediction)

    match max_index:
        #***************** NEEED TO CHANGE THESES *************
        #Angry
        case 0:
            emotion_recognized = "Angry"

        #Digust
        case 1:
            emotion_recognized = "Disgust"

        #Fear
        case 2:
            ingredient_recognized = "Fear"

        #Happy
        case 3:
            ingredient_recognized = "Happy"

        #Neutral
        case 4:
            ingredient_recognized = "Neutral"

        #Sad
        case 5:
            ingredient_recognized = "Sad"

        #Surpised
        case 6:
            ingredient_recognized = "Surpised"
    
    print("Ingredient: ", ingredient_recognized, " Confidence: ", confidence*100,"%")

    #Setting confidence greater than 50% to enact change
    if(confidence > .50):

        #************** NEED TO CHANGE THIS
        if(emotion_recognized == "Sad" or emotion_recognized == "Angry" or emotion_recognized == "Disgust"):
            action = 0

        elif(emotion_recognized == "Happy"):
            action = 100

        else:
            action = 50
    else:
        print("[LOG] Confidence level was below 50%. Discarding data")

    return action

    
def external_control_loop():


    prediction = recognize_ingredient()

    #Returning Change to PSO Algorithm
    action = decodePrediction(prediction)

    return action

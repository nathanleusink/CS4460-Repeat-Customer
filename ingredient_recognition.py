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
import random

#Special Modules needed from keras for CNN
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

# Init Camera
video_capture = cv2.VideoCapture(0)
ret, frames = video_capture.read() 

def getCameraFrame():
    global frames
    
    #Getting Single Frame from Camera and converting it to gray scale
    ret, frames = video_capture.read()
    gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)    

    return gray
    
def getTestImage():

    global frames

    
    #Paths
    base_dir = os.getcwd()
    training_data_path = base_dir + "\\ingredient_test_images"

    lettuce_path = training_data_path + "\\lettuce\\"
    onion_path = training_data_path + "\\onions\\"
    meat_path = training_data_path + "\\meat\\"
    cheese_path = training_data_path + "\\cheese\\"
    tomato_path = training_data_path + "\\tomatoes\\"
    moldy_lettuce_path = training_data_path + "\\moldy lettuce\\"
    moldy_onion_path = training_data_path + "\\moldy onion\\"
    moldy_meat_path = training_data_path + "\\moldy meat\\"
    moldy_cheese_path = training_data_path + "\\moldy cheese\\"
    moldy_tomato_path = training_data_path + "\\moldy tomatoes\\"

    keras.layers.InputLayer(input_shape=(224, 224, 1))

    path = ""

    #Deciding if Lettuce Moldy or not then chosing image
    rand_num = random.randint(0, 10)
    if(rand_num != 0):
        lettuce = random.choice(os.listdir(lettuce_path))
        path = lettuce_path
    else:
        lettuce = random.choice(os.listdir(moldy_lettuce_path))
        path = moldy_lettuce_path
    lettuce_img = Image.open(path + lettuce)

    #Deciding if Onion Moldy or not then chosing image
    rand_num = random.randint(0, 10)
    if(rand_num != 0):
        onion = random.choice(os.listdir(onion_path))
        path = onion_path
    else:
        onion = random.choice(os.listdir(moldy_onion_path))
        path = moldy_onion_path
    onion_img = Image.open(path + onion)

    #Deciding if Meat Moldy or not then chosing image
    rand_num = random.randint(0, 10)
    if(rand_num != 0):
        meat = random.choice(os.listdir(meat_path))
        path = meat_path
    else:
        meat = random.choice(os.listdir(moldy_meat_path))
        path = moldy_meat_path
    meat_img = Image.open(path + meat)

    #Deciding if Cheese Moldy or not then chosing image
    rand_num = random.randint(0, 10)
    if(rand_num != 0):
        cheese = random.choice(os.listdir(cheese_path))
        path = cheese_path
    else:
        cheese = random.choice(os.listdir(moldy_cheese_path))
        path = moldy_cheese_path
    cheese_img = Image.open(path + cheese)

    #Deciding if Tomato Moldy or not then chosing image
    rand_num = random.randint(0, 10)
    if(rand_num != 0):
        tomato = random.choice(os.listdir(tomato_path))
        path = tomato_path
    else:
        tomato = random.choice(os.listdir(moldy_tomato_path))
        path = moldy_tomato_path
    tomato_img = Image.open(path + tomato)

    #Load Image --> Convert to Gray Scale --> Resize to 224 by 224 pixels
    print("[LOG] Formatting Input.")
    meat_img = meat_img.resize((224,224))
    cheese_img = cheese_img.resize((224,224))
    tomato_img = tomato_img.resize((224,224))
    onion_img = onion_img.resize((224,224))
    lettuce_img = lettuce_img.resize((224,224))

    #Converting Image to Numpy Array
    meat_array = np.array(meat_img)
    cheese_array = np.array(cheese_img)
    tomato_array = np.array(tomato_img)
    onion_array = np.array(onion_img)
    lettuce_array = np.array(lettuce_img)
    
    
    #Expanding Matching Tensor 4D Shape
    meat_array = np.expand_dims(meat_array, axis=0)
    cheese_array = np.expand_dims(cheese_array, axis=0)
    tomato_array = np.expand_dims(tomato_array, axis=0)
    onion_array = np.expand_dims(onion_array, axis=0)
    lettuce_array = np.expand_dims(lettuce_array, axis=0)

    array_list = []
    array_list.append(meat_array)
    array_list.append(cheese_array)
    array_list.append(tomato_array)
    array_list.append(onion_array)
    array_list.append(lettuce_array)
    
    return array_list
    
def recognize_ingredient():
    
    ### Ingredient Recognition ###

    global frames

    ####
    #IF USING A LIVE IMAGE
    #gray = getCameraFrame()
    #
    # IF USING A TEST IMAGE
    array_list = getTestImage()
    ####
    
    #Loading CNN For Ingredient Recognition
    print("[LOG] Loading CNN Model... ")
    base_path = os.getcwd()
    model = keras.models.load_model(base_path + '\\ingredient_cnn.h5')
    print("[LOG] CNN Model Loaded.")

    #Making Prediction
    print("[LOG] Making Prediction")
    for value in array_list:
        prediction = model.predict(value)
        good_result = decodePrediction(prediction)
        
    return good_result

def decodePrediction(prediction):

    ingredient_recognized = ""
    ingredient_good = False
    
    confidence = np.amax(prediction)
    max_index = np.argmax(prediction)


    match max_index:
        case 0:
            ingredient_recognized = "Cheese"
        case 1:
            ingredient_recognized = "Letuce"
        case 2:
            ingredient_recognized = "Meat"
        case 3:
            ingredient_recognized = "Moldy Lettuce"
        case 4:
            ingredient_recognized = "Moldy Meat"
        case 5:
            ingredient_recognized = "Moldy Onion"
        case 6:
            ingredient_recognized = "Moldy Tomatoes"
        case 7:
            ingredient_recognized = "Moldy Onions"
        case 8:
            ingredient_recognized = "Onions"
        case 9:
            ingredient_recognized = "Tomatoes"
            

    print("Ingredient: ", ingredient_recognized, " Confidence: ", confidence*100,"%")

    #Setting confidence greater than 50% to enact change
    if(confidence > .50):
        if(ingredient_recognized.find("*Moldy*")):
            ingredient_good = False
        else:
            ingredient_good = True
    else:
        print("[LOG] Confidence level was below 50%. Discarding data")

    return ingredient_good

import os
import random

#Import Statements
import cv2
import numpy as np
from PIL import Image, ImageOps
from keras import models
import tensorflow as tf
import time

#Special Modules needed from keras for CNN
from tensorflow import keras
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions


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


sandwich_ingredient_list = []
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


sandwich_ingredient_list.append(lettuce_img)
sandwich_ingredient_list.append(onion_img)
sandwich_ingredient_list.append(meat_img)
sandwich_ingredient_list.append(cheese_img)
sandwich_ingredient_list.append(tomato_img)
print(sandwich_ingredient_list)

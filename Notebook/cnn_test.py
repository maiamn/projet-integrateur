# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 08:14:49 2022

@author: Ellias
"""

#TensorFlow – Importing the Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import tensorflow as tf

import keras

#TensorFlow – Getting and Splitting the Dataset

path_to_photos = "./archive/img_align_celeba/img_align_celeba"
csv_attributes = "./archive/list_attr_celeba.csv"

data = pd.read_csv(csv_attributes, index_col=0)

#print(data[["Arched_Eyebrows","Young"]].head(3))
npdata = data.to_numpy()


'''
img_names = data["image_id"].tolist()

print(img_names)

'''

img = tf.keras.utils.load_img(path_to_photos + "/000001.jpg")
print((img))
print(img.format)
print(img.size)

img = img.resize([30, 30])
print(img.size)

img_array = tf.keras.utils.img_to_array(img)
print(img_array[0])
print(img_array.shape)
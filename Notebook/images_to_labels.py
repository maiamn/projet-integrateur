#!/usr/bin/env python
# coding: utf-8

# In[25]:


#f = "/home/ingargio/projet/test"
#MODEL_PATH = "/home/ingargio/saved_model_50000/cp.h5"


# In[9]:


import os
import pandas as pd
import string
import random
import matplotlib
import numpy as np
#import coremltools
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#get_ipython().run_line_magic('matplotlib', 'inline')
from keras import backend as K
from ast import literal_eval
from sklearn.utils import class_weight
from keras.models import Sequential
from keras.models import load_model
from keras.metrics import top_k_categorical_accuracy
from keras.callbacks import ModelCheckpoint
from keras_preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Activation, Flatten, Dropout, BatchNormalization, GlobalAveragePooling2D
from keras.layers import Conv2D, MaxPooling2D
from keras import regularizers, optimizers
from livelossplot import PlotLossesKeras
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
import PIL
import os
import os.path
from PIL import Image
from keras.preprocessing.image import ImageDataGenerator
from keras.applications.vgg16 import preprocess_input
from keras.utils import load_img
from keras.utils import img_to_array


# In[10]:


def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall

def precision(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision

def f1(y_true, y_pred):
    p = precision(y_true, y_pred)
    r = recall(y_true, y_pred)
    return 2*((p*r)/(p++K.epsilon()))


# In[11]:


def get_model(path):
    print("Récupération du modèle")
    model = load_model(path, custom_objects={"f1": f1, "recall": recall,"precision": precision})
    return model


# In[12]:


def resize_images(path):
    for files in os.listdir(path):
        f_img = path+"/"+files
        img = Image.open(f_img)
        img = img.resize((224,224))
        img.save(f_img)
    print("Images resized !")


# In[31]:


def predict_labels(model,images,unique_labels):
    predictions =  []
    images_path = []
    labels_images = []
    best_labels = []
    seuil_confiance = 40
    
    data = {j:[] for j in unique_labels}
    data['image_id']= []

    for file in images.keys():
        img = images[file]
        print("mon image ", img)
        my_image = Image.open(img)
        my_image = my_image.resize((224,224))

        #preprocess the image
        my_image = img_to_array(my_image)
        my_image = my_image.reshape((1, my_image.shape[0], my_image.shape[1], my_image.shape[2]))
        my_image = preprocess_input(my_image)

        #make the prediction
        pred_values = model.predict(my_image)
        predictions.append(pred_values)
        images_path.append(file)
        data['image_id'].append(file)

        #enregistre les meilleurs labels
        best = []
        labels = []
        
        print(len(pred_values[0]))
        for i in range(len(pred_values[0])):
            if pred_values[0][i]*100 > seuil_confiance :
                best.append(unique_labels[i] + " %.1f" % (pred_values[0][i]*100) + "%")
                data[unique_labels[i]].append(1)
            else :
                data[unique_labels[i]].append(-1)
            labels.append(unique_labels[i] + " %.1f" % (pred_values[0][i]*100) + "%")

        best_labels.append(best)
        labels_images.append(labels)
        
    for image in range(len(images_path)):  
        print(images_path[image])
        print("Best labels : ")
        print(best_labels[image]) 

    return data


# In[29]:


def predicted(model_path,images):
    
    unique_labels = ['5_o_Clock_Shadow',
     'Bags_Under_Eyes',
     'Bald',
     'Bangs',
     'Big_Lips',
     'Big_Nose',
     'Black_Hair',
     'Blond_Hair',
     'Brown_Hair',
     'Bushy_Eyebrows',
     'Chubby',
     'Eyeglasses',
     'Goatee',
     'Gray_Hair',
     'Heavy_Makeup',
     'High_Cheekbones',
     'Male',
     'Mouth_Slightly_Open',
     'Mustache',
     'No_Beard',
     'Oval_Face',
     'Pale_Skin',
     'Pointy_Nose',
     'Receding_Hairline',
     'Rosy_Cheeks',
     'Sideburns',
     'Smiling',
     'Straight_Hair',
     'Wavy_Hair',
     'Wearing_Earrings',
     'Wearing_Hat',
     'Wearing_Lipstick',
     'Wearing_Necklace',
     'Wearing_Necktie',
     'Young']
        
    model = get_model(model_path)
    data = predict_labels(model,images,unique_labels)
    
    df = pd.DataFrame(data,
               columns =['image_id']+unique_labels)
    return df


# In[32]:


#df = predicted(MODEL_PATH,f)
#df


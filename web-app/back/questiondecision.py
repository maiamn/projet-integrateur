import csv
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from random import randint
from IPython.display import display



# Global variables
last_training = 162770
last_validation = 182637
last_testing = 202599
max_data = 1000

fname="D:/INSA/5A/Cours/Projet SDBD/Projet intégrateur/CelebA/list_attr_celeba.csv"

# Echelle de subjectivité de 1 à 3
labels_weights = {
    'Male':1,
    'Young':2,
    'Eyeglasses':1,
    'Wearing_Necktie':1,
    'Wearing_Necklace':1,
    'Wearing_Earrings':1,
    'Wearing_Hat':1,
    'Big_Lips':3,
    'Big_Nose':3,
    'Bags_Under_Eyes':3,
    'Bushy_Eyebrows':3,
    'Wearing_Lipstick':2,
    'Heavy_Makeup':2,
    'Smiling':1,
    'Mouth_Slightly_Open':2,
    'Receding_Hairline':2,
    'Bald':1,
    'Blond_Hair':1,
    'Brown_Hair':1,
    'Black_Hair':1,
    'Gray_Hair':1,
    'Bangs':2,
    'Wavy_Hair':3,
    'Straight_Hair':3,
    'No_Beard':1,
    '5_o_Clock_Shadow':2,
    'Goatee':2,
    'Mustache':1,
    'Sideburns':2,
    'Pale_Skin':3,
    'Rosy_Cheeks':3,
    'Pointy_Nose':3,
    'Chubby':3,
    'High_Cheekbones':3,
    'Oval_Face':3    
}

questions={
    'Male':"Is it a boy?",
    'Young':"Are they young?",
    'Eyeglasses':"Do they wear eyeglasses?",
    'Wearing_Necktie':"Do they wear a tie?",
    'Wearing_Necklace':"Do they wear a necklace?",
    'Wearing_Earrings':"Do they wear earrings?",
    'Wearing_Hat':"Do they wear a hat?",
    'Big_Lips':"Do they have big lips?",
    'Big_Nose':"Do they have a big nose?",
    'Bags_Under_Eyes':"Do they have bags under their eyes?",
    'Bushy_Eyebrows':"Do they have bushy eyebrows?",
    'Wearing_Lipstick':"Do they wear lipstick?",
    'Heavy_Makeup':"Do they wear heavy makeup?",
    'Smiling':"Do they smile?",
    'Mouth_Slightly_Open':"Do they have their mouth slightly open?",
    'Receding_Hairline':"Do they have a receding hairline?",
    'Bald':"Are they bald?",
    'Blond_Hair':"Do they have blond hair?",
    'Brown_Hair':"Do they have brown hair?",
    'Black_Hair':"Do they have black hair?",
    'Gray_Hair':"Do they have gray hair?",
    'Bangs':"Do they have bangs?",
    'Wavy_Hair':"Do they have wavy hair?",
    'Straight_Hair':"Do they have straight hair?",
    'No_Beard':"Do they have no beard?",
    '5_o_Clock_Shadow':"Do they have a 5 o’clock shadow?",
    'Goatee':"Do they have a goatee?",
    'Mustache':"Do they have a mustache?",
    'Sideburns':"Do they have sideburns?",
    'Pale_Skin':"Do they have pale skin?",
    'Rosy_Cheeks':"Do they have rosy cheeks?",
    'Pointy_Nose':"Do they have a pointy nose?",
    'Chubby':"Are they chubby?",
    'High_Cheekbones':"Do they have high cheekbones?",
    'Oval_Face':"Do they have an oval face?"    
}

labels = [ 'image_id', '5_o_Clock_Shadow', 'Bags_Under_Eyes', 'Bald', 'Bangs', 'Big_Lips',
 'Big_Nose', 'Black_Hair', 'Blond_Hair', 'Brown_Hair', 'Bushy_Eyebrows',
 'Chubby', 'Eyeglasses', 'Goatee', 'Gray_Hair', 'Heavy_Makeup',
 'High_Cheekbones', 'Male', 'Mouth_Slightly_Open', 'Mustache', 'No_Beard',
 'Oval_Face', 'Pale_Skin', 'Pointy_Nose', 'Receding_Hairline', 'Rosy_Cheeks',
 'Sideburns', 'Smiling', 'Straight_Hair', 'Wavy_Hair', 'Wearing_Earrings',
 'Wearing_Hat', 'Wearing_Lipstick', 'Wearing_Necklace', 'Wearing_Necktie',
 'Young'
]

# Recuperer les données depuis le fichier csv 
def init_data():
    data = np.genfromtxt(fname, dtype=str, delimiter=",")
    data1 = data[:,0:2]
    data2 = data[:,4:11]
    data3 = data[:,12:15]
    data4 = data[:,16:24]
    data5 = data[:,25:]

    global newdata
    newdata = np.concatenate((data1,data2,data3,data4,data5), axis=1)
    return newdata

# Recuperer les labels
def init_labels():
    global labels 
    labels = init_data()[0]

# Construction du dataframe
def construct_dataframe():
    global myDataFrame 
    myDataFrame = pd.DataFrame(columns=labels)

    new_entry={}

    for i in range(0,max_data):
        for j in range(len(labels)):
            new_entry[labels[j]] = newdata[i][j]

        myDataFrame = myDataFrame.append(new_entry, ignore_index=True)

    myDataFrame.sort_values(by="image_id")
    return myDataFrame

# Initialisation
def init():
    init_data()
    init_labels()
    construct_dataframe()

# Given the nb of the image (ex:456) returns the image_id corresponding (ex:"000456.jpg")
def get_jpg_name(id):
    name=""
    nb_of_zeros = 6-len(str(id))
    for i in range(nb_of_zeros):
        name += "0"
    name += str(id)
    name += ".jpg"
    return name

def get_id_from_jpg(jpg_name):
    id = jpg_name[:6]
    return int(id)

def construct_dataframe_from_ids(list_id):  
    myDataFrame = pd.DataFrame(columns=labels)
    new_entry={}
    for i in list_id:
        for j in range(len(labels)):
            new_entry[labels[j]] = newdata[i][j]

        myDataFrame = myDataFrame.append(new_entry, ignore_index=True)
    return myDataFrame

def construct_dataframe_from_jpg_names(list_jpg):  
    myDataFrame = pd.DataFrame(columns=labels)
    new_entry={}
    for i in list_jpg:
        for j in range(len(labels)):
            new_entry[labels[j]] = newdata[get_id_from_jpg(i)][j]

        myDataFrame = myDataFrame.append(new_entry, ignore_index=True)
    return myDataFrame

def get_labels_img_as_list(nb_image):
    if type(nb_image) is int:
        return myDataFrame.loc[myDataFrame['image_id']==get_jpg_name(nb_image)].values.tolist()[0][1:]
    else:
        return myDataFrame.loc[myDataFrame['image_id']==nb_image].values.tolist()[0][1:]

def get_n_images_df(n):
    randomImages = []
    while len(randomImages)<n:
        different_labels=True
        r = randint(0,max_data)
        for i in range(len(randomImages)):
            #check if there are >=2 images with the same labels
            if get_labels_img_as_list(r) == get_labels_img_as_list(randomImages[i]):
                different_labels=False
                break
        if different_labels:
            randomImages.append(get_jpg_name(r))
    
    return(myDataFrame.loc[myDataFrame['image_id'].isin(randomImages)].sort_values(by="image_id"))

def get_n_images_jpg_name(n):
    randomImages = []
    while len(randomImages)<n:
        different_labels=True
        r = randint(0,max_data)
        for i in range(len(randomImages)):
            #check if there are >=2 images with the same labels
            if get_labels_img_as_list(r) == get_labels_img_as_list(randomImages[i]):
                different_labels=False
                break
        if different_labels:
            randomImages.append(get_jpg_name(r))
    
    return(randomImages)

def get_images_left_df(images_before, label_question, answer):
    label_answer = '1' if answer else '-1'
    return images_before.loc[images_before[label_question] == label_answer].sort_values(by="image_id")

def choose_question(df,excluded_labels):
    score_min = 2
    label_min = ""
    
    #evaluate all scores + find the best one
    for label in df:
        print(label)
        if label != 'image_id' and label not in excluded_labels:
            nb_positive = get_images_left_df(df, label, 1)
            score_rep = abs(len(nb_positive.values.tolist())/len(df.values.tolist())-0.5)+1
            score = score_rep * labels_weights[label]
            if (score < score_min):
                score_min = score
                label_min = label
    return(label_min)

def test():
    df=get_n_images_df(20)
    display(df)
    
    label_question = ""
    while len(df) > 1 :
        label_question = choose_question(df)
        print(label_question)
        new_df = get_images_left_df(df, label_question, 1)
        df = new_df
        display(df)

    return label_question


################  Fonctions modifiées pour être utilisées dans le microservices  ########################
def get_question_to_ask(list_images,excluded_labels): 
    df = json_to_dataframe(list_images)
    print(df)
    label = choose_question(df,excluded_labels)
    return (questions[label]) 


def json_to_dataframe(list_images):
    myDataFrame = pd.DataFrame(columns=labels)

    att_to_crop = ["Attractive","Blurry","Double_Chin", "Arched_Eyebrows", "Narrow_Eyes"]

    for img in list_images['labels'].keys():
        for i in att_to_crop :
            if i in list_images['labels'][img].keys():
                del list_images['labels'][img][i]
        list_images['labels'][img]["image_id"] = img
        
        myDataFrame = myDataFrame.append(list_images['labels'][img], ignore_index=True)
    return myDataFrame
##########################################################################################################

if __name__ == '__main__':
    init()
    test()
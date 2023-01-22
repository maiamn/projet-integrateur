###########################################################################################################
# Python script to load the images contained in a folder (as well as the labels) to the couchDB database  #                                                           #
# Change the path variable with the path of the folder where the images are                               #                                                           #  
###########################################################################################################

import os
import couchdb
import pandas as pd
import numpy as np

# path where images are stored
path = r'C:\Users\Elise\Documents\5SDBD\projet-integrateur\Notebook\Ressources_Test\images_test'
files_list = os.listdir(path)

# path where labels are stored
path_labels = r'C:\Users\Elise\Documents\5SDBD\projet-integrateur\Notebook\Ressources_Test\list_attr_celeba.csv'
data = pd.read_csv(path_labels, index_col=0)
npdata = data.to_numpy()

# connection to CouchDB
couch = couchdb.Server("http://user:user@localhost:5984") # http://login:password@localhost:5984
couch.create("images")
db = couch['images'] # images = name of the database

n = 5 # Number of subset
for i in range(n) :
    files_list_subset = files_list[i * int(len(files_list)/n) : (i+1) * int(len(files_list)/n)]
    dic = data.iloc[i * int(len(files_list)/n) : (i+1) * int(len(files_list)/n)].to_dict(orient='index')
    
    for file in files_list_subset:
        # saving a new doc for each image in the database
        doc = {'_id': file, 'labels': dic[file]}
        db.save(doc)
        doc = db.get(file)
        # attaching the image to the doc
        slash = "\\"
        file_path = path + slash + file
        f = open(file_path, "rb")
        db.put_attachment(doc=doc, content=f, filename=file, content_type="image/jpg")
        f.close() 
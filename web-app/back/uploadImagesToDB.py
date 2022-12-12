###################################################################################
# Python script to load the images contained in a folder to the couchDB database  #                                                           #
# Change the path variable with the path of the folder where the images are       #                                                           #  
###################################################################################

import os
import couchdb

# path where images are stored
path = r'C:\Users\Elise\Documents\5SDBD\projet-integrateur\Notebook\Ressources_Test\images_test'

files_list = os.listdir(path)

# connection to CouchDB
couch = couchdb.Server("http://user:user@localhost:5984") # http://login:password@localhost:5984
db = couch['images'] # images = name of the database


for file in files_list:
    # saving a new doc for each image in the database
    doc = {'_id': file}
    db.save(doc)
    doc = db.get(file)
    # attaching the image to the doc
    slash = "\\"
    file_path = path + slash + file
    f = open(file_path, "rb")
    db.put_attachment(doc=doc, content=f, filename=file, content_type="image/jpg")
    f.close()
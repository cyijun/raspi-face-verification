from deepface import DeepFace
from deepface.basemodels import VGGFace
import tensorflow as tf
import os
import json

my_model = None
json_file = open("./model/model.json", 'r')
tf.keras.models.model_from_json = json_file.read()
json_file.close()

my_model = VGGFace.loadModel()

try:
    #img1Vec=DeepFace.represent(img_path="new.jpg", model = my_model)
    # print(img1Vec)
    #result = DeepFace.verify(img1_path="new.jpg", img2_path="photo.jpg", model = my_model, distance_metric='euclidean_l2')
    faceVecDict = {
        'treenewbee': {
            "foo":[],
            "bar":[],
            "ugh":[],
        }
    }
    faceVecDict['treenewbee']['foo']=DeepFace.represent(img_path="image/foo.jpg", model = my_model)
    faceVecDict['treenewbee']['bar']=DeepFace.represent(img_path="image/bar.jpg", model = my_model)
    faceVecDict['treenewbee']['ugh']=DeepFace.represent(img_path="image/ugh.jpg", model = my_model)
    
    with open('face_set.json', 'w+') as face_vec_file:
        face_vec_file.write(json.dumps(faceVecDict))
    
except KeyboardInterrupt:
    pass

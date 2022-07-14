from deepface import DeepFace
from deepface.basemodels import VGGFace
from deepface.commons import distance as dst

import numpy as np
import tensorflow as tf
import os
import json
import gc

DIST_THRESHOLD = 0.86

face_vec_file = open('face_set.json', 'r')
faceVecs = json.loads(face_vec_file.read())
face_vec_file.close()

my_model = None
json_file = open("./model/model.json", 'r')
tf.keras.models.model_from_json = json_file.read()
json_file.close()

my_model = VGGFace.loadModel()

def save_model_to_json():
    model_json = my_model.to_json()
    with open('model.json', "w") as json_file:
        json_file.write(model_json)
    json_file.close()

faceSet = faceVecs['treenewbee']

def my_verify(img_path="./image/photo.jpg"):
    isFace = True
    try:
        inputImgVec = DeepFace.represent(img_path=img_path, model=my_model, detector_backend='ssd')
    except ValueError as ve:
        if str(ve).find('Face could not be detected.') != -1:
            isFace = False

    if isFace:
        for name, vec in faceSet.items():
            dist = dst.findEuclideanDistance(dst.l2_normalize(vec), dst.l2_normalize(inputImgVec))
            dist = np.float64(dist)

            if dist < DIST_THRESHOLD:
                resultDict = {}
                resultDict['name'] = name
                resultDict['dist'] = dist
                return(resultDict)
                
        resultDict = {}
        resultDict['name'] = 'Unknown'
        print(resultDict)
        return resultDict

    else:
        resultDict = {}
        resultDict['name'] = 'NoFace'
        print(resultDict)
        return resultDict

def release_resources():
    del my_model
    tf.keras.backend.clear_session()
    gc.collect()

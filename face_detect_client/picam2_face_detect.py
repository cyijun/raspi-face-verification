# coding: utf-8

from picamera2 import Picamera2, Preview, MappedArray

import requests
import cv2 as cv2
import base64
import time
import json
import numpy as np

from virtual_sensor import mqtt_loop_start, setToDefaultState

url = "http://your_inference_server_addr:9960/face_verify"


def getRealName(resp) -> str:
    respDict = json.loads(resp)
    realName = respDict["name"]
    return realName


def searchFacesByBase64(img, url):

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    _, jpg_data = cv2.imencode('.jpg', img, encode_param)

    jpg_as_text = base64.b64encode(jpg_data)

    try:
        myobj = {'frame': jpg_as_text}

        x = requests.post(url, json=myobj)

        print(x.text)
        return x.text
    except Exception as e:
        print(str(e))
        return None


def detectedCallback(request):
    with MappedArray(request, "main") as m:
        for f in faces:
            name = getRealName(searchFacesByBase64(m.array, url))
            name = name.lower().replace(' ', '_')
            print(name)
            if name != 'noface':
                setToDefaultState(name,10)


# Load the cascade
face_cascade = cv2.CascadeClassifier(
    '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml')

#tuning = Picamera2.load_tuning_file(
#    "/usr/share/libcamera/ipa/raspberrypi/imx219_noir.json")
#picam2 = Picamera2(tuning=tuning)

picam2 = Picamera2()

picam2.configure(picam2.preview_configuration(main={"size": (3280, 2464)},
                                              lores={"size": (320, 240), "format": "YUV420"}))

#(w0, h0) = picam2.stream_configuration("main")["size"]
(w1, h1) = picam2.stream_configuration("lores")["size"]
s_haar = picam2.stream_configuration("lores")["stride"]

faces = []

picam2.post_callback = detectedCallback

picam2.start()

mqtt_loop_start()

while True:
    buffer = picam2.capture_buffer("lores")
    grey = buffer[:s_haar * h1].reshape((h1, s_haar))
    faces = face_cascade.detectMultiScale(grey, 1.1, 1)

from flask import Flask
from flask import request

import face_verify

import base64
import json

from virtual_sensor_server import mqtt_loop_start, publish_as_sensor

cache_dir='./'

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/face_verify", methods=['GET', 'POST'])
def verify_face():
    if request.method == 'POST':
        received=request.json
        imgBytes=base64.b64decode(received['frame'])
        with open(cache_dir+'cache.jpg','wb+') as cache_file:
            cache_file.write(imgBytes)
        resp=face_verify.my_verify(cache_dir+'cache.jpg')
        print(resp)
        publish_as_sensor(resp)
        return json.dumps(resp)
    return "<p>error</p>"

if __name__ == '__main__':
    mqtt_loop_start()
    app.run(host="0.0.0.0", port=9960)
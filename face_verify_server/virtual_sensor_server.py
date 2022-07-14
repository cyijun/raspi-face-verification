

import logging
import sys
import time
import json
import base64
import paho.mqtt.client as mqtt
from face_verify import faceSet
import threading

def on_connect(mqtt_client, obj, flags, rc):
    #mqtt_client.publish('pi/state','online',retain=True)

    nameList=[]
    for name,vec in faceSet.items():
        nameList.append(name)
    nameList.append('Unknown')

    for name in nameList:
        name=name.lower().replace(' ', '_')
        mqtt_client.publish('homeassistant/binary_sensor/pi001/'+name+'_detection/config',
        '{"availability":[{"topic":"pi/state"}],"device":{"identifiers":["pi-pi001"],"manufacturer":"Raspberry","model":"pi 1.0","name":"pi001","sw_version":"1.0.0"},"name":"pi001 '+name+'_detection","unique_id":"pi001_'+name+'_detection_pi","device_class":"presence","state_topic":"pi/'+name+'/detected","payload_on":"on","payload_off":"off"}',retain=True)

def mqtt_loop_start():
    client.loop_start()

def setToDefaultState(tname,name,delay):
    client.publish('pi/'+name+'/detected','off',retain=True)

def publish_as_sensor(resp:dict):
    for name,vec in faceSet.items():
        if name == resp['name']:
            name=name.lower().replace(' ', '_')
            client.publish('pi/'+name+'/detected','on',retain=True)
            break

client = mqtt.Client('face_server')
client.on_connect = on_connect
client.connect('your_mqtt_server_addr', 1883,keepalive=5)
#client.subscribe('pi/detected', qos=0)
#client.will_set('pi/state','offline',retain=True)
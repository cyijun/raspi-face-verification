

import logging
import sys
import time
import json
import base64
import paho.mqtt.client as mqtt


def on_connect(mqtt_client, obj, flags, rc):
    mqtt_client.publish('pi/state', 'online', retain=True)


def setToDefaultState(name, delay=120):
    print('detected, sleep for a while')
    time.sleep(delay)
    client.publish('pi/'+name+'/detected', 'off', retain=True)


def mqtt_loop_start():
    client.loop_start()


client = mqtt.Client('pi')
client.on_connect = on_connect
client.connect('your_mqtt_server_addr', 1883, keepalive=5)
#client.subscribe('pi/detected', qos=0)
client.will_set('pi/state', 'offline', retain=True)
client.subscribe('pi/#')

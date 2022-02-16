#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
from setup import *

# This is the test publisher

BROKER_ADDRESS = get_broker_addr()

client = mqtt.Client()
client.connect(BROKER_ADDRESS,1883,60)

def on_message(client, userdata, msg):
    print("got message")
    print("topic:", msg.topic)
    print("content:", msg.payload.decode())

client.on_message = on_message

client.subscribe("thresholds")

while True:
    time.sleep(5)
    print("sending message")
    client.publish("readings", '{"Sensor0":89.69,"Sensor1":22,"Sensor2":11.1}')
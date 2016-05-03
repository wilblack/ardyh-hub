import json

import paho.mqtt.client as mqtt

from tornado.websocket import WebSocketClosedError


from sensor_db import Db
db = Db()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    bot_topics = [
        ("ardyh/bots/rpi1", 0),
        ("ardyh/bots/rpi2", 0),
        ("ardyh/bots/rpi3", 0),
        ("ardyh/bots/rpi4", 0)
    ]
    client.subscribe(bot_topics)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    
    msgObj = json.loads(msg.payload)
    if not 'handshake' in msgObj.keys():
        
        lux = msgObj.get('lux', None)
        light = msgObj.get('light', None)
        vals = [msgObj['temp'], msgObj['humidity'], light, lux]
        db.update(msg.topic, vals)


class MqttLogger(object):

    def __init__(self, broker_url, broker_port):

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        print "MgttLogger.__init__() Trying to connect to %s" %(broker_url)
        self.client.connect(broker_url, 1883, 60)

        print "Starting mqtt self.client"
        self.client.loop_start()


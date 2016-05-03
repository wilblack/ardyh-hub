"""
This is ardyh
Tornado Websockts server used the pass for lilybots.

Wil Black, wilblack21@gmail.com 
Oct. 26, 2013



## Messages

- message
    -- name
    -- from
    -- message
    -- command
    -- channel
    -- ardyh_timestamp - May not be present


"""
import sys, json, ast, math, os
import time 
import collections
import datetime
from datetime import datetime as dt

import paho.mqtt.client as mqtt

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.websocket import WebSocketClosedError
import tornado.template


# Settings
VERBOSE = True
PORT = 9093
ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
IP = "192.168.0.105"
ARDYH_MONITOR = 'monitor.solalla.ardyh'

MQTT_BROKER_URL = "192.168.0.105"
MQTT_BROKER_PORT = 1883

PATH = os.path.dirname(os.path.abspath(__file__))
# End Settings


from sensor_db import Db
db = Db()

from mqtt_client import MqttLogger
mqtt_logger = MqttLogger(MQTT_BROKER_URL, MQTT_BROKER_PORT)


def start_mqtt_cient(socket):

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
        # TODO Clean out NaN's here.
        # send messages over web socket
        try:
            json.dumps(msgObj, allow_nan=False)
        except ValueError:
            print "****  MESSAGE HAS NAN's", msg.payload

        try:
            socket.write_message({"topic": msg.topic, "payload": msgObj})
        except WebSocketClosedError:
            print "Web socket was closed."


    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_BROKER_URL, 1883, 60)

    print "Starting mqtt client"
    client.loop_start()
    return client



# This stores the socket connections
listeners = []
def get_bot_listener(bot_name):
    return next( ([i,bot] for i, bot in enumerate(listeners) if bot['bot_name'] == bot_name), [None, None] )


class HubWebRequestHandler(tornado.web.RequestHandler):

    def set_default_headers(self):

        print "setting headers"
        self.set_header("Access-Control-Allow-Origin", "*")


class MainHandler(HubWebRequestHandler):

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


    def get(self, action=None, *args, **kwargs):
        """
        Displays the webpage.

        Endpoints

          **/api/sensors/BOT.NAME/?start=START-TS&end=END-TS**
          
          **/api/bot/**
          This endpoint lists all bots connected to via web socket.
        """

        print "In MainHandler"
        pieces = action.strip("/").split("/")

        if pieces[0] == 'sensors':
            assert len(pieces) == 2, "Invalid url, sensor endpoit is /api/sensors/BOT-NAME"
            
            # Get start and end date filters and convert datetime objects
            start = self.get_argument('start', None)
            end = self.get_argument('end', None)
            

            bot = pieces[1]
            rs = db.fetch(bot, start, end)
            #out = json.dumps(rs)
            out = {'results':rs}
            self.write(out)

        elif pieces[0] == "bot":
            temp = []
            for l in listeners:
                row = {
                    'bot_name': l.get('bot_name', None),
                    'bot_roles': l.get('bot_roles', None),
                    'mac': l.get('mac', ''),
                    'local_ip': l.get('local_ip', ''),
                    'subscriptions': l.get('subscriptions', ''),
                    'sensors': l.get('sensors', []),
                }
                temp.append(row)

            out = json.dumps(temp)
            self.write(out)

        elif pieces[0] == "device":
            """
            Endpoint 

            /api/device/MAC-ADDRESS/

            """
            mac = pieces[1]

            start = self.get_argument('start', None)
            end = self.get_argument('end', None)

            rs = db.fetch_device(mac, start, end)
            out = {'results':rs}
            self.write(out)

        else:
            loader = tornado.template.Loader(".")
            self.write(loader.load("templates/index.html").generate())



class WSHandler(tornado.websocket.WebSocketHandler):

    def __init__(self, application, request, **kwargs):
        super(WSHandler, self).__init__(application, request, **kwargs)

        # Set attach the sokcet to the mqqt client
        self.mqtt = start_mqtt_cient(self)

    def check_origin(self, origin):
        return True

    def open(self):
        """
        Bots should connect with a query string containing the bot name

        i.e. ws://IP-ADDRESS:PORT/?ardyh.bots.rpi1

        It will than append or update the bot in the listeners array

        """

        print "Connection opened..."

        try:
            bot_name = self.request.uri.split("?")[1]
        except:
            bot_name = ""
        print "Hello from %s" %bot_name

        self.bot_name = bot_name
        i, old_socket = get_bot_listener(bot_name)
        if old_socket:
            old_socket.update({'socket':self})
        else:
            bot = {
                "socket": self,
                "subscriptions": [],
                "bot_name": bot_name
            }

            listeners.append( bot )
            self.log('Sucessfully established socket connection')


    def on_message(self, message):
        """
        Tries to forward commands to the appropruate mqtt channel (botName).

        This receives messages as strings. message is then loaded into python.
        It will look for a keyword named "command" in the message object.

        If it has a command, it will look for a 'botName', in kwargs. The botName should
        be the mqtt channel and it will be used to publish an object containing
        the a command, kwargs key/val pairs. These should be picked up in rpi_client.


        """
        # print "[WSHandler.on_message] message ", message
        # Need to catch these and route the to the apropriate mqtt channel.
        message = json.loads(message);
        if 'command' in message.keys():
            cmd = message['command']
            kwargs = message['kwargs']
            channel = kwargs.get('botName', None)
            if channel:
                payload = {
                    'command': cmd,
                    'kwargs': kwargs
                }
                self.mqtt.publish(channel, json.dumps(payload))

        #channel = message.botName
        #payload = message.data
        #



    def on_close(self):
        print 'Lost connection closed.'
        self.mqtt.disconnect()



application = tornado.web.Application([
      (r'/ws', WSHandler),
      #(r'/', MainHandler),
      (r'/api/(.*)', MainHandler),
      (r"/(.*)", tornado.web.StaticFileHandler, {'path':os.path.join(PATH, 'homeMonitor/dist')}),
    ])


if __name__ == "__main__":
    #r = redis.StrictRedis(host='localhost', port=6379, db=0)

    print "Starting HTTP server at %s:%s" %(IP, PORT) 
    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(PORT) 
    application.listen(PORT)

    print "Starting Websocket server at ws://%s:%s" %(IP, PORT)          #starts the websockets connection
    tornado.ioloop.IOLoop.instance().start()


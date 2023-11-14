import sys
import time
from Adafruit_IO import MQTTClient
from Adafruit_IO import *
import Port
class Task3:
    AIO_FEED_IDs = ["buttonmultiplelight", "buttonsinglelight"]
    AIO_USERNAME = "PhamBaoLongGroupAI"
    AIO_KEY = ""

    def connected(self, client):
        print("Connect successfully ...")
        for feed in self.AIO_FEED_IDs:
            client.subscribe(feed)
            #client.publish(feed, 0)

    def subscribe(self, client , userdata , mid , granted_qos):
        print("Subscribe!!!")

    def disconnected(self, client):
        print("Disconnected ...")
        sys.exit (1)

    def message(self, client , feed_id , payload):
        #print("Received payload: " + payload)
        #print("Received feed_id:" + feed_id)
        if feed_id == 'buttonsinglelight':
            if payload == "1":
                print(".")
                Port.sendCommand("4")
                return

            elif payload == "0":
                Port.sendCommand("5")
                return

        if feed_id == 'buttonmultiplelight':
            if payload == "1":
                print("-")
                Port.sendCommand("1")
                return

            elif payload == "0":
                Port.sendCommand("0")
                return

    def execute(self, client):
        time.sleep(0.1)
        Port.sendCommand("1")
        return

    def __init__(self):
        client = MQTTClient(self.AIO_USERNAME , self.AIO_KEY)
        client.on_connect = self.connected
        client.on_disconnect = self.disconnected
        client.on_message = self.message
        client.on_subscribe = self.subscribe
        client.connect()
        client.loop_background()

task3 = Task3()
while True:
    pass

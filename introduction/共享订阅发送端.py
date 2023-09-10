#!/usr/bin/python
# -*- coding: utf-8 -*-

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv5
import time
from paho import mqtt


class Demo(object):
    def __init__(self, host, port, client_id, publishTopic) -> None:
        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv5)
        self.handClient.connect_async(host, port)
        self.handClient.on_connect = self.on_connect
        self.publishTopic = publishTopic

    def on_connect(self, client, userdata, flags, reasonCode, properties):
        if reasonCode == 0:
            print("链接成功")

    def loop(self):
        while True:
            time.sleep(1)
            message = time.strftime("%X")
            self.handClient.publish(self.publishTopic, message)

    def run(self):
        self.handClient.loop_start()
        self.loop()

    def __del__(self):
        self.handClient.disconnect()


if __name__ == "__main__":
    # 客户端id
    client_id = "publish"
    host = "localhost"
    port = 1883
    publishTopic = "topic"
    try:
        D = Demo(client_id=client_id, host=host, port=port, publishTopic=publishTopic)
        D.run()
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

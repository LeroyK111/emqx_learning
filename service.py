#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
! 实验mqtt通讯
"""

from paho.mqtt import client as mqtt_client
import random


class Demo(object):
    def __init__(self, host, port, topic, client_id) -> None:
        self.handClient = mqtt_client.Client(client_id=client_id)
        self.handClient.connect(host, port)
        # 失败回调
        self.handClient.on_connect = self.on_connect
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def subscribe(self):
        # 等待接受
        def on_message(client, userdata, msg):
            print(f"接收 `{msg.payload.decode()}` 来自 `{msg.topic}`")

        # 订阅这个主题
        self.handClient.subscribe(self.topic)
        # 回调函数
        self.handClient.on_message = on_message

    def loopStart(self):
        self.handClient.loop_forever()


if __name__ == "__main__":
    broker = "localhost"
    port = 1883
    # topic = "/python/mqtt"
    topic = "devices/+/messages"
    client_id = f"python-mqtt-{random.randint(0, 1000)}"
    try:
        D = Demo(broker, port, topic, client_id)
        D.subscribe()
        D.loopStart()
    except KeyboardInterrupt:
        print("结束运行")

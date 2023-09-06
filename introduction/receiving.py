#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
* 这里是当前目录所有客户端的接收端

mqtt主要是还是发报端定义消息的特殊功能。挺好的。
"""


from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv5


class Demo(object):
    def __init__(self, client_id, host, port):
        # 接受参数，初始化链接, 我们选择mqtt5做为常用协议。
        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv5, transport="tcp")
        # 监听订阅是否成功，也受到 connect_async 影响
        self.handClient.on_subscribe = self.on_subscribe
        # 消息回调
        self.handClient.on_message = self.on_message
        # !存在bug，订阅消息是阻塞
        self.handClient.connect(host, port)

    def on_subscribe(self, client, userdata, mid, reasonCodes, properties):
        print("订阅成功")

    def on_message(self, client, userdata, message):
        print(f"{message.topic} to {message.payload.decode()}")

    def receiveMessages(self, topic):
        self.handClient.subscribe(topic)
        # self.handClient.loop_forever()
        self.handClient.loop_start()


if __name__ == "__main__":
    # 客户端id
    client_id = "noGame"
    host = "10.102.220.223"
    port = 1883
    try:
        D = Demo(client_id, host, port)
        # 接受消息
        D.receiveMessages("retain")
    except Exception as identifier:
        print(identifier)
    except KeyboardInterrupt:
        print("手动中断监听")

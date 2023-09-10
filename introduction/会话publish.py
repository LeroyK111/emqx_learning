#!/usr/bin/python
# -*- coding: utf-8 -*-

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv311


class Demo(object):
    def __init__(self, client_id, host, port):
        self.client_id = client_id
        self.host = host
        self.port = port
        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv311, transport="tcp")
        self.handClient.connect(host, port)

    def sendMessage(self, topic):
        for i in range(3):
            self.handClient.publish(topic, "保存会话", qos=1)


if __name__ == "__main__":
    # 客户端id
    client_id = "setGame"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id, host, port)
        # 接受消息
        D.sendMessage("clean_session_false")
    except Exception as identifier:
        print(identifier)
    except KeyboardInterrupt:
        print("手动中断监听")
    else:
        print("结束")

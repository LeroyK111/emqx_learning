#!/usr/bin/python
# -*- coding: utf-8 -*-


from paho.mqtt import client as mqtt_client

# 获取mqtt版本
from paho.mqtt.client import MQTTv311
import paho.mqtt.subscribe as subscribe

"""

"""


class Demo(object):
    def __init__(self, host, port, client_id) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id
        # 创建实例
        self.handClient = mqtt_client.Client(client_id=self.client_id, protocol=MQTTv311, transport="tcp", clean_session=False)

    # 开启链接
    def openConnect(self):
        self.handClient.connect(self.host, self.port)

    # 断开链接
    def closeConnect(self):
        self.handClient.disconnect()

    # 接收消息
    def callbackMessage(self, topic):
        def on_message_print(client, userdata, message):
            print("主题是%s，消息是%s" % (message.topic, message.payload.decode("utf-8")))

        subscribe.callback(on_message_print, topic, qos=0, userdata=None, hostname=self.host, port=self.port, client_id=self.client_id, keepalive=60, will=None, auth=None, tls=None, protocol=MQTTv311)


if __name__ == "__main__":
    # 客户端id
    client_id = "getGame"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id=client_id, host=host, port=port)
        D.callbackMessage("clean_session_false")
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

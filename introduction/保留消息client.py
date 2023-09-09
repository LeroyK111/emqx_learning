#!/usr/bin/python
# -*- coding: utf-8 -*-


from paho.mqtt import client as mqtt_client

# 获取mqtt版本
from paho.mqtt.client import MQTTv311

# 全局辅助函数
from paho.mqtt.client import connack_string

import time
from datetime import datetime as dt

# 调用单条发送
import paho.mqtt.publish as publish

"""
保留消息：当 MQTT 客户端向服务器发布消息时，可以设置保留消息标志。保留消息存储在消息服务器上，后续订阅该主题的客户端仍然可以收到该消息。
只保留客户端发出的最后一条消息。

! 设置mqtt版本 默认是3.1.1
MQTTv31 = 3
MQTTv311 = 4
MQTTv5 = 5

! 设置mqtt链接方式，默认是tcp
transport = tcp || websocket
"""


class Demo(object):
    def __init__(self, host, port, client_id) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id
        # 创建实例
        self.handClient = mqtt_client.Client(client_id=self.client_id, protocol=MQTTv311, transport="tcp")
        # 同步链接
        # self.handClient.connect(host, port)
        # 使用异步链接
        self.handClient.connect_async(host, port)
        # 回调函数, 只适合同步链接监听
        self.handClient.on_connect = self.on_connect
        # 开启异步事件
        self.handClient.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        """
        client：客户端实例
        userdata：用户私有数据
        flags: 代理发送标志
        rc: 链接结果
        """
        if rc == 0:
            print("链接状态", connack_string(rc))
            
        else:
            print("Failed to connect, return code %d\n", rc)

    # 发送消息
    def sendMessage(self, topic):
        # retain 开启保留消息
        while True:
            time.sleep(1)
            # socket = self.handClient.socket()
            # print(dir(socket))
            message = f"保留消息{dt.today()}"
            result = self.handClient.publish(topic, message, retain=True, qos=0)

    def single_send_message(self, topic):
        while True:
            time.sleep(.1)
            message = f"保留消息{dt.today()}"
            publish.single(topic, payload=message, qos=0, retain=True, hostname=self.host, port=self.port, client_id=self.client_id, keepalive=60, will=None, auth=None, tls=None, protocol=MQTTv311, transport="tcp")

    def multiple_send_message(self, topic):
        while True:
            time.sleep(0.1)
            # 多条报文格式，列表嵌套元素+字典
            msgs = [{"topic": topic, "payload": "multiple 1", "retain": True}, (topic + "1", "multiple 2", 0, True)]
            publish.multiple(msgs, hostname=self.host, port=self.port)


if __name__ == "__main__":
    # 客户端id
    client_id = "getGame"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id=client_id, host=host, port=port)
        # 常规发报文
        D.sendMessage("retain")
        # 发报文，单条
        # D.single_send_message("retain")
        # 发报文，多条
        # D.multiple_send_message("retain")
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

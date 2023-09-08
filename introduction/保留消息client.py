#!/usr/bin/python
# -*- coding: utf-8 -*-


from paho.mqtt import client as mqtt_client

# 获取mqtt版本
from paho.mqtt.client import MQTTv311

# 全局辅助函数
from paho.mqtt.client import connack_string

import time
from datetime import datetime as dt

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
        # 创建实例
        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv311, transport="tcp")
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
            time.sleep(0.1)
            message = f"保留消息{dt.today()}"
            result = self.handClient.publish(topic, message, retain=True, qos=0)
            # if result[0] == 0:
            #     print(f"发送成功, {message}")


if __name__ == "__main__":
    # 客户端id
    client_id = "getGame"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id=client_id, host=host, port=port)
        # 发消息
        D.sendMessage("retain")
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

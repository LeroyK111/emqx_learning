#!/usr/bin/python
# -*- coding: utf-8 -*-


from paho.mqtt import client as mqtt_client

# 获取mqtt版本
from paho.mqtt.client import MQTTv311

# 全局辅助函数
from paho.mqtt.client import connack_string
import time
from datetime import datetime as dt


class Demo(object):
    def __init__(self, host, port, client_id) -> None:
        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv311, transport="tcp")
        self.handClient.connect_async(host, port)
        self.handClient.on_connect = self.on_connect
        self.handClient.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("链接状态", connack_string(rc))
        else:
            print("Failed to connect, return code %d\n", rc)

    # 发送消息
    def sendMessage(self, topic):
        while True:
            time.sleep(0.1)
            message = f"保留消息{dt.today()}"
            result = self.handClient.publish(topic, message, retain=True, qos=0)


if __name__ == "__main__":
    # 客户端id
    client_id = "getGame"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id=client_id, host=host, port=port)
        D.sendMessage("retain")
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

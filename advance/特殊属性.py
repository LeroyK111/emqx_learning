#!/usr/bin/python
# -*- coding: utf-8 -*-


from paho.mqtt import client as mqtt_client

# 获取mqtt版本
from paho.mqtt.client import MQTTv5

# 全局辅助函数
from paho.mqtt.client import connack_string
import time
from datetime import datetime as dt

OPTIONS = {
    "properties": {
        "userProperties": {
            "region": "A",
            "type": "JSON",
        },
    },
}


class Demo(object):
    def __init__(self, host, port, client_id) -> None:
        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv5, transport="tcp", userdata={"username": "leroy", "password": "password"})
        # 链接时，用户自定义的信息
        self.handClient.connect_async(host, port, properties=OPTIONS["properties"], keepalive=600)
        self.handClient.on_connect = self.on_connect
        self.handClient.loop_start()

    def on_connect(self, client, userdata, flags, reasonCode, properties):
        if reasonCode == 0:
            print("链接状态", connack_string(reasonCode))
            print("打印额外信息, {}".format(properties))
        else:
            print("Failed to connect, return code %d\n", reasonCode)

    # 发送消息
    def sendMessage(self, topic):
        while True:
            time.sleep(0.1)
            message = f"保留消息{dt.today()}"
            # 发布消息时。传递额外信息
            result = self.handClient.publish(topic, message, retain=True, qos=0, properties=OPTIONS["properties"])


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

#!/usr/bin/python
# -*- coding: utf-8 -*-


from asyncio import timeout
from paho.mqtt import client as mqtt_client

# 获取mqtt版本
from paho.mqtt.client import MQTTv311


class Demo(object):
    def __init__(self, host, port, client_id) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id
        # 创建实例
        self.handClient = mqtt_client.Client(
            client_id=self.client_id,
            protocol=MQTTv311,
            transport="tcp"
        )
        self.handClient.on_publish = self.on_publish

    def on_publish(self, client, userdata, mid):
        print(mid)

    # 开启链接
    def openConnect(self, topic):
        # 直接设置遗嘱消息
        self.handClient.will_set(topic, "遗嘱消息", qos=1)
        self.handClient.connect(self.host, self.port, keepalive=5)

    # 断开链接
    def closeConnect(self):
        self.handClient.disconnect()


if __name__ == "__main__":
    # 客户端id
    client_id = "Last Will"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id=client_id, host=host, port=port)
        D.openConnect("last_will")
        D.closeConnect()
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

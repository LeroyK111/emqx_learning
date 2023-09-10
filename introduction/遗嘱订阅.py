#!/usr/bin/python
# -*- coding: utf-8 -*-


from paho.mqtt import client as mqtt_client

# 获取mqtt版本
from paho.mqtt.client import MQTTv311


class Demo(object):
    def __init__(self, host, port, client_id) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id
        # 创建实例
        self.handClient = mqtt_client.Client(client_id=self.client_id, protocol=MQTTv311, transport="tcp", clean_session=False)
        self.handClient.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        print(msg.topic + "消息：" + msg.payload.decode("utf-8"))

    # 开启链接
    def openConnect(self, topic):
        self.handClient.connect(self.host, self.port)
        self.handClient.subscribe(topic, qos=1)

    # 断开链接
    def closeConnect(self):
        self.handClient.disconnect()

    def startLoop(self):
        self.handClient.loop_forever()


if __name__ == "__main__":
    # 客户端id
    client_id = "Simple Demo"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id=client_id, host=host, port=port)
        D.openConnect("last_will")
        D.startLoop()
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

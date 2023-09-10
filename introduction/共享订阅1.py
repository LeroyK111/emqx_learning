#!/usr/bin/python
# -*- coding: utf-8 -*-

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv5


class Demo(object):
    def __init__(self, host, port, client_id, subscribeTopic) -> None:
        self.host = host
        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv5)
        self.handClient.on_connect = self.on_connect
        self.handClient.on_message = self.on_message
        self.handClient.connect_async(host, port)
        self.subscribeTopic = subscribeTopic

    def on_connect(self, client, userdata, flags, reasonCode, properties):
        if reasonCode == 0:
            print("链接成功")
            self.handClient.subscribe(self.subscribeTopic)

    def on_message(self, client, userdata, message):
        self.globalObj = message.payload.decode("utf-8")
        print(f"{message.topic} 的 {self.globalObj}")

    def run(self):
        self.handClient.loop_forever()

    def __del__(self):
        self.handClient.loop_stop()


if __name__ == "__main__":
    # 客户端id
    host = "localhost"
    port = 1883
    subscribeTopic = "$share/g/topic"
    try:
        D = Demo(client_id=None, host=host, port=port, subscribeTopic=subscribeTopic)
        D.run()
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

#!/usr/bin/python
# -*- coding: utf-8 -*-


from paho.mqtt import client as mqtt_client
import json
import time


class Demo(object):
    def __init__(self, host, port, client_id, subscribeTopic, publishTopic) -> None:
        self.host = host
        self.handClient = mqtt_client.Client(client_id=client_id)
        self.handClient.on_connect = self.on_connect
        self.handClient.on_message = self.on_message
        self.handClient.connect_async(host, port, keepalive=600)
        self.publishTopic = publishTopic
        self.subscribeTopic = subscribeTopic
        self.globalObj = None

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("链接成功")
            self.handClient.subscribe(self.subscribeTopic)

    def on_message(self, client, userdata, message):
        self.globalObj = message.payload.decode("utf-8")
        print(f"{message.topic} 的 {self.globalObj}")

    def loop(self):
        while True:
            time.sleep(.1)
            message = '{"temperature": 40, "humidity": 20}'
            # 发送成功
            self.handClient.publish(self.publishTopic, message, qos=1, retain=True)

    def run(self):
        self.handClient.loop_start()
        self.loop()

    def __del__(self):
        self.handClient.disconnect()


if __name__ == "__main__":
    # 客户端id
    client_id = "ekuiper quick test"
    host = "localhost"
    port = 1883
    publishTopic = "devices/device_001/messages"
    subscribeTopic = "leroy"
    try:
        D = Demo(client_id=client_id, host=host, port=port, subscribeTopic=subscribeTopic, publishTopic=publishTopic)
        D.run()
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
todo 使用docker拉取emqt服务。
* docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:latest
* http://localhost:18083/ admin public

! pip install paho-mqtt hbmqtt gmqtt
我们选择paho-mqtt。

使用 1883 端口的 TCP 类型监听器
使用 8883 端口的 SSL/TLS 安全连接类型监听器
使用 8083 端口的 WebSocket 类型监听器
使用 8084 端口的 WebSocket 安全类型监听器
18083: emqt web管理页面
"""

from paho.mqtt import client as mqtt_client
import random
import time


class Demo(object):
    def __init__(self, host, port, topic, client_id) -> None:
        # 创建实例
        self.handClient = mqtt_client.Client(client_id=client_id, clean_session=False)
        self.handClient.connect(host, port)
        # 失败回调
        self.handClient.on_connect = self.on_connect
        # 开启异步
        self.handClient.loop_start()
        self.topic = topic

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def publish(self):
        # 循环发送消息
        msg_count = 0
        while True:
            # time.sleep(0.1)
            msg = f"messages: {msg_count}"
            result = self.handClient.publish(self.topic, msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"发送 `{msg}` 到信道 `{self.topic}`")
            else:
                print(f"发送失败的信道 {self.topic}")
            msg_count += 1


if __name__ == "__main__":
    broker = "192.168.1.51"
    port = 1883
    topic = "/python/mqtt"
    client_id = f"python-mqtt-{random.randint(0, 1000)}"
    try:
        D = Demo(broker, port, topic, client_id)
        D.publish()
    except KeyboardInterrupt:
        print("结束运行")

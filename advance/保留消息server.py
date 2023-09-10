#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
* 这里是当前目录所有客户端的接收端

mqtt主要是还是发报端定义消息的特殊功能。挺好的。
"""

# 异步订阅

from paho.mqtt import client as mqtt_client
from paho.mqtt.client import MQTTv311

# 独立订阅
import paho.mqtt.subscribe as subscribe

# 独立发送
import paho.mqtt.publish as publish
from paho.mqtt.client import connack_string, topic_matches_sub, error_string

# 偏函数
from functools import partial


class Demo(object):
    def __init__(self, client_id, host, port):
        self.client_id = client_id
        self.host = host
        self.port = port
        # 接受参数，初始化链接, 我们选择mqtt5做为常用协议。
        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv311, transport="tcp")
        # 监听订阅是否成功，也受到 connect_async 影响
        # self.handClient.on_subscribe = self.on_subscribe
        # !存在bug，订阅消息是阻塞状态，如果你
        # self.handClient.connect(host, port)
        self.handClient.connect_async(host, port)
        # 消息回调
        self.handClient.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc, **kwargs):
        if rc == 0:
            print("链接状态", connack_string(rc))
            # 异步则放到这里订阅。
            self.handClient.subscribe(kwargs["topic"])
        else:
            print("Failed to connect, return code %d\n", error_string(rc))

    def on_message(self, client, userdata, message):
        """
        dup: 消息是否重复
        info: 元数据
        mid：计数器
        payload：消息内容
        properties：携带参数，一般是标识符
        qos：消息等级
        retain: 保留消息标志符
        state: 消息状态码, 反应消息处在哪个阶段
        timestamp：收到信息的时间戳
        topic：主题/信道
        """
        if message.retain == 1:
            print("此消息是保留消息")
        else:
            print("此消息非保留消息")

    def receive_message(self, topic):
        # 同步可以这么直接使用订阅。
        # self.handClient.subscribe(topic)
        Adv_on_connect = partial(self.on_connect, topic=topic)
        # 链接监听
        self.handClient.on_connect = Adv_on_connect
        # 推荐订阅方式
        self.handClient.loop_forever()


if __name__ == "__main__":
    # 客户端id
    client_id = "receive"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id, host, port)
        D.receive_message("retain")
    except Exception as identifier:
        print(identifier)
    except KeyboardInterrupt:
        print("手动中断监听")

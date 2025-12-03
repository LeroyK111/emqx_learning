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

# 订阅选项
import paho.mqtt.subscribeoptions as SubscribeOptions

# 特殊标志位
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes

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
            """
            QoS: 订阅端进行qos等级限制
            
            No Local：真则，不允许消息转发给这个消息的发送客户端，避免转发风暴
            
            Retain As Published： 只有 0 和 1 两个可取值，为 1 表示服务端在向此订阅转发应用消息时需要保持消息中的 Retain 标识不变，为 0 则表示必须清除。
            
            将 Retain Handling 设置为 0，表示只要订阅建立，就发送保留消息；

            将 Retain Handling 设置为 1，表示只有建立全新的订阅而不是重复订阅时，才发送保留消息；

            将 Retain Handling 设置为 2，表示订阅建立时不要发送保留消息。
            """
            # 设置订阅的标识符
            publish_properties = Properties(PacketTypes.SUBSCRIBE)
            publish_properties.UserProperty = ("Subscription Identifier", "1")
            
            self.handClient.subscribe(kwargs["topic"], options=SubscribeOptions(qos=1, noLocal=1, retainAsPublished=1, retainHandling=1), properties=publish_properties)
        else:
            print("Failed to connect, return code %d\n", error_string(rc))

    def on_message(self, client, userdata, message):
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

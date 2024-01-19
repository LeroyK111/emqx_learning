#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
* 这里是当前目录所有客户端的接收端

mqtt主要是还是发报端定义消息的特殊功能。挺好的。
"""

# 异步订阅
from base64 import decode
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
        """
        client：客户端实例
        userdata：用户私有数据
        flags: 代理发送标志
        rc: 链接结果
        """
        if rc == 0:
            print("链接状态", connack_string(rc))
            # 异步则放到这里订阅。
            self.handClient.subscribe(kwargs['topic'])
        else:
            print("Failed to connect, return code %d\n", error_string(rc))

    def on_message(self, client, userdata, message):
        print(f"{message.topic} to {message.payload.decode()}")

    def receive_message(self, topic):
        # 同步可以这么直接使用订阅。
        # self.handClient.subscribe(topic)
        Adv_on_connect = partial(self.on_connect, topic=topic)
        # 链接监听
        self.handClient.on_connect = Adv_on_connect
        # 推荐订阅方式
        self.handClient.loop_forever()

    def single_receive_message(self, topic):
        """
        ! 单条订阅
        topics订阅主题:字符串or列表or元组
        qos 质量：0，1，2
        msg_count: 接收条数
        retained: 如果接收到的是，保留消息，则特殊标注
        hostname: 服务地址
        port: 服务端口
        client_id: 客户端名字
        keepalive: 链接存活时间

        will: "will"参数用于设置遗嘱消息（Last Will and Testament，简称LWT） {'topic': "<topic>", 'payload':"<payload">, 'qos':<qos>, 'retain':<retain>}.

        auth: {'username':"<username>", 'password':"<password>"} 账户密码

        tls: 证书，ssh密钥文件

        protocol: mqtt版本3，4，5

        transport协议类型: tcp or websocket

        clean_session: mqtt5不再使用清除会话的概念

        proxy_args代理emqx：
        """
        # 使用单条接收
        msg = subscribe.simple(
            topics=topic, qos=0, msg_count=1, retained=False, hostname=self.host, port=self.port, client_id=self.client_id, keepalive=60, will=None, auth=None, tls=None, protocol=MQTTv311, transport="tcp", clean_session=False, proxy_args=None
        )
        print(msg.payload.decode("utf-8"))
        # for m in msg:
        #     print(m.payload.decode("utf-8"))

    def callbackMessage(self, topic):
        def on_message_print(client, userdata, message):
            print("主题是%s，消息是%s" % (message.topic, message.payload.decode("utf-8")))

        subscribe.callback(on_message_print, topic, qos=0, userdata=None, hostname=self.host, port=self.port, client_id=self.client_id, keepalive=60, will=None, auth=None, tls=None, protocol=MQTTv311)


if __name__ == "__main__":
    # 客户端id
    client_id = "receive"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id, host, port)
        # 接受消息
        D.receive_message("retain")
        # 魔改的话，这两个好下手
        # 独立单条订阅
        # D.single_receive_message("retain")
        # 独立回调订阅
        # D.callbackMessage("retain")
    except Exception as identifier:
        print(identifier)
    except KeyboardInterrupt:
        print("手动中断监听")

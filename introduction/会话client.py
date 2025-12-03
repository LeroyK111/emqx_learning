#!/usr/bin/python
# -*- coding: utf-8 -*-


from paho.mqtt import client as mqtt_client

# 获取mqtt版本
from paho.mqtt.client import MQTTv311

# !获取额外传参属性 mqttv5
from paho.mqtt.properties import Properties
from paho.mqtt.packettypes import PacketTypes



class Demo(object):
    def __init__(self, host, port, client_id) -> None:
        self.host = host
        self.port = port
        self.client_id = client_id
        # 创建实例
        self.handClient = mqtt_client.Client(client_id=self.client_id, protocol=MQTTv311, transport="tcp", clean_session=False)
        self.handClient.on_message = self.on_message

    # def __init__(self, host, port, client_id) -> None:
    #     self.host = host
    #     self.port = port
    #     self.client_id = client_id
    #     # 创建实例, v5版本没有clean_session 完全是由连接器定义
    #     self.handClient = mqtt_client.Client(client_id=self.client_id, protocol=MQTTv5, transport="tcp")
    #     self.handClient.on_message = self.on_message

    def on_message(self, client, userdata, msg):
        print(msg.topic + "消息：" + msg.payload.decode("utf-8"))

    # 开启链接
    def openConnect(self, topic):
        self.handClient.connect(self.host, self.port)
        
        
        # publish_properties = Properties(PacketTypes.PUBLISH)
        # 设置会话过期时间
        # publish_properties.UserProperty = {"Session Expiry Interval": 60}
        # self.handClient.connect(self.host, self.port, clean_start=0, properties=publish_properties)
        
        
        self.handClient.subscribe(topic, qos=1)

    # 断开链接
    def closeConnect(self):
        self.handClient.disconnect()

    def startLoop(self):
        self.handClient.loop_forever()


if __name__ == "__main__":
    # 客户端id
    client_id = "getGame"
    host = "localhost"
    port = 1883
    try:
        D = Demo(client_id=client_id, host=host, port=port)
        D.openConnect("clean_session_false")
        # 当会话publish发送三条消息到这个topic， 这个信道就会缓存这个会话。直到被再次订阅。一旦订阅了成功，就会清空缓存数据。
        D.startLoop()
    except Exception as error:
        print(error)
    except KeyboardInterrupt:
        print("手动中断")
    else:
        print("结束")

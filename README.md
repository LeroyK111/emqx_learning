# EMQX学习笔记

官网：https://www.emqx.io/zh
教程：https://www.emqx.com/zh/mqtt-guide

## 背景

物联网专用：
MQTT（Message Queuing Telemetry Transport，消息队列遥测传输协议），是一种基于`发布/订阅`（`publish/subscribe`）模式的“轻量级”通讯协议，该协议构建于TCP/IP协议上，由IBM在1999年发布。
MQTT最大优点在于，**用极少的代码和有限的带宽，为连接远程设备提供实时可靠的消息服务**。
作为一种低开销、低带宽占用的即时通讯协议，使其在物联网、小型设备、移动应用等方面有较广泛的应用。

MQTT代理的主流应用
- Mosquitto：https://mosquitto.org/
    
- VerneMQ：https://vernemq.com/
    
- EMQTT：http://emqtt.io/

### 版本
- MQTT v3.1.0 
	- 目前已经不常用了
- MQTT v3.1.1 
	- 常用版本
	- 差异：https://github.com/mqtt/mqtt.org/wiki/Differences-between-3.1.0-and-3.1.1
	- 支持websocket
- MQTT v5 
	- 没有v4版本，是因为v3.1.1才应该叫4。😀
	- 2018年正式发布。
- **MQTT-SN**
	- 针对嵌入式设备提出的协议
	-  2013 年发布，通过**UDP**、ZigBee 和其他传输方式工作

### 层级
MQTT 与 HTTP 一样，MQTT 运行在传输控制协议/互联网协议 (TCP/IP) 堆栈之上。
![](readme.assets/Pasted%20image%2020230829225215.png)

### 发布和订阅的原理
`MQTT`使用的发布/订阅消息模式，它提供了一对多的消息分发机制，从而实现与应用程序的解耦。
这是一种消息传递模式，**消息不是直接从发送器发送到接收器**（即点对点），而是由`MQTT server`（或称为 MQTT Broker）分发的。
![](readme.assets/Pasted%20image%2020230829225705.png)
**MQTT  Broker 是发布-订阅架构的核心**。

#### 订阅选项
当你有三方数据集成时，就需要参考订阅选项。
订阅选项server.py
```python
#!/usr/bin/python

# -*- coding: utf-8 -*-

  
  

from paho.mqtt import client as mqtt_client

from paho.mqtt.client import MQTTv311

  

# 独立订阅

import paho.mqtt.subscribe as subscribe

  

# 订阅选项

import paho.mqtt.subscribeoptions as SubscribeOptions

  

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

            self.handClient.subscribe(kwargs["topic"], options=SubscribeOptions(qos=1, noLocal=1, retainAsPublished=1, retainHandling=1))

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
```


### 设置Qos质量
QoS（Quality of Service levels）
服务质量是 MQTT 的一个重要特性。当我们使用 TCP/IP 时，连接已经在一定程度上受到保护。但是在无线网络中，中断和干扰很频繁，MQTT 在这里帮助避免信息丢失及其服务质量水平。这些级别在发布时使用。如果客户端发布到 MQTT 服务器，则客户端将是发送者，MQTT 服务器将是接收者。当MQTT服务器向客户端发布消息时，服务器是发送者，客户端是接收者。

**QoS  0**
这一级别会发生消息丢失或重复，消息发布依赖于底层TCP/IP网络。即：<=1
![](readme.assets/Pasted%20image%2020230829230220.png)

**QoS  1**
QoS 1 承诺消息将至少传送一次给订阅者。
![](readme.assets/Pasted%20image%2020230829230246.png)

**QoS  2**

使用 QoS 2，我们保证消息仅传送到目的地一次。为此，带有唯一消息 ID 的消息会存储两次，首先来自发送者，然后是接收者。QoS 级别 2 在网络中具有最高的开销，因为在发送方和接收方之间需要两个流。
![](readme.assets/Pasted%20image%2020230829230315.png)

### MQTT数据包结构

![](readme.assets/Pasted%20image%2020230910195246.png)

- `固定头（Fixed header）`，存在于所有`MQTT`数据包中，表示数据包类型及数据包的分组类标识；
- `可变头（Variable header）`，存在于部分`MQTT`数据包中，数据包类型决定了可变头是否存在及其具体内容；
- `消息体（Payload）`，存在于部分`MQTT`数据包中，表示客户端收到的具体内容；
![](readme.assets/Pasted%20image%2020230829230551.png)
![](readme.assets/Pasted%20image%2020230829230753.png)
![](readme.assets/Pasted%20image%2020230829230815.png)
![](readme.assets/Pasted%20image%2020230829230843.png)
![](readme.assets/Pasted%20image%2020230829231017.png)
![](readme.assets/Pasted%20image%2020230829231046.png)




## EMQX的架构
EMQX 是一款[开源 (opens new window)](https://github.com/emqx/emqx)的大规模分布式 MQTT 消息服务器，功能丰富，专为物联网和实时通信应用而设计。EMQX 5.0 单集群支持 MQTT 并发连接数高达 1 亿条，单服务器的传输与处理吞吐量可达每秒百万级 MQTT 消息，并保证延迟在亚毫秒级。

EMQX 支持多种协议，包括 MQTT (3.1、3.1.1 和 5.0)、HTTP、QUIC 和 WebSocket 等，保证各种网络环境和硬件设备的可访问性。EMQX 还提供了全面的 SSL/TLS 功能支持，比如双向认证以及多种身份验证机制，为物联网设备和应用程序提供可靠和高效的通信基础设施。

内置基于 SQL 的[规则引擎 (opens new window)](https://www.emqx.com/zh/solutions/iot-rule-engine)，EMQX 可以实时提取、过滤、丰富和转换物联网数据。此外，EMQX 采用了无主分布式架构，以确保高可用性和水平扩展性，并提供操作友好的用户体验和出色的可观测性。

- 支持Mria 集群架构
- 热更新
- 支持下一代协议QUIC
- 备份与恢复
- EMQX 5.x 的规则引擎在原有 SQL 的基础上集成了 [jq (opens new window)](https://stedolan.github.io/jq/)，支持更多复杂格式 JSON 数据的处理。
- 认证授权
- 过载保护、速率限制器和桥接缓存队列



### 安装EMQX
EMQX 支持多种安装方式，比如[容器化部署](https://www.emqx.io/docs/zh/v5.1/deploy/install-docker.html)，通过 [EMQX Kubernetes Operator (opens new window)](https://www.emqx.com/zh/emqx-kubernetes-operator)安装部署、或通过安装包的形式部署在物理服务器或虚拟机上。

这里我们为了学习，使用docker容器化部署单节点的方式，开发mqtt应用。

官方web测试平台：http://www.emqx.io/online-mqtt-client#/recent_connections
  
- 使用 1883 端口的 TCP 类型监听器
- 使用 8883 端口的 SSL/TLS 安全连接类型监听器
- 使用 8083 端口的 WebSocket 类型监听器
- 使用 8084 端口的 WebSocket 安全类型监听器
- 使用18083端口: web管理页面
```shell
$ docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:latest
```

控制台地址： http://localhost:18083/
​默认用户名，密码：admin，public

#### 使用官方客户端测试
os端：https://mqttx.app/zh
web端：http://www.emqx.io/online-mqtt-client#/recent_connections
![](readme.assets/Pasted%20image%2020230905122832.png)
##### 初始化配置
![](readme.assets/Pasted%20image%2020230905124935.png)
![](readme.assets/Pasted%20image%2020230905125554.png)

##### 操作面板
![](readme.assets/Pasted%20image%2020230905125902.png)
![](readme.assets/Pasted%20image%2020230905130256.png)
![](readme.assets/Pasted%20image%2020230905131959.png)
剩下的就随便玩吧。
#### ekuiper流处理器
会使用 ekuiper 作为流数据处理，过滤筛选，组合排列，读写存储数据。
```shell
$ docker pull lfedge/ekuiper
```

开源版本不支持数据持久化。需要自己写数据库。

|**描述**|**配额**|
|---|---|
|**设备连接**||
|最大并发连接设备数|不限|
|最大设备建立连接速度|不限|
|最大客户端 ID 长度|65535|
|**设备订阅**||
|最大订阅数|不限|
|最大订阅速度|不限|
|单个设备订阅数|不限|
|单个设备订阅速度|不限|
|**网络流量**||
|最大带宽|不限|
|单个设备带宽|不限|
|**MQTT 消息**||
|单条消息大小|默认 1024KB，最大 256MB|
|最大 QoS|2|
|**MQTT 心跳时长**||
|支持设置的最大心跳时长|65535 秒|
|**MQTT 主题**||
|主题数量|不限|
|主题层级|65535|
|主题长度|不限|
|支持的主题别名数量|65535|
|**MQTT 保留消息**||
|单条消息大小|默认 1204KB，最大 256MB|
|保留消息总数|不限|
|保留消息总大小|不限|
|**MQTT 5.0 协议**||
|最多可添加用户自定义属性个数|65535|
|**MQTT 扩展**||
|主题重写规则数量|30|
|代理订阅规则数量|30|
|延迟发布消息数量|不限|
|延迟发布最大时长|4294967秒|
|**规则引擎**||
|规则数量|不限|
|规则执行超时|不限|
|单个规则目的地数量|不限|
|**数据桥接**||
|数据桥接数量|不限|
|**REST API**||
|分页最大大小|10000|
|API 密钥数量|100|
|**Dashboard**||
|Dashboard 用户数量|不限|

### 常见问题支持
https://www.emqx.io/docs/zh/v5.1/faq/faq.html

### 部署和迁移
https://www.emqx.io/docs/zh/v5.1/deploy/install.html
- Docker-Compose：容器管家，只能管理当前主机的容器
- Docker Swarm:  **docker 专用的跨主机的容器管理平台**
- Kubernetes：**跨容器，跨主机的容器管理平台**

#### 集群
https://www.emqx.io/docs/zh/v5.1/deploy/cluster/introduction.html

涉及的目录

|目录|描述|压缩包解压安装|二进制包安装|
|---|---|---|---|
|`etc`|配置文件目录|`./etc`|`/etc/emqx`|
|`data`|数据文件|`./data`|`/var/lib/emqx`|
|`log`|日志文件|`./log`|`/var/log/emqx`|
|`releases`|启动相关的脚本|`./releases`|`/usr/lib/emqx/releases`|
|`bin`|可执行文件目录|`./bin`|`/usr/lib/emqx/bin`|
|`lib`|Erlang 代码|`./lib`|`/usr/lib/emqx/lib`|
|`erts-*`|Erlang 虚拟机文件|`./erts-*`|`/usr/lib/emqx/erts-*`|
|`plugins`|插件|`./plugins`|`/usr/lib/emqx/plugins`|
1. 压缩包解压安装时，目录相对于软件所在目录；
2. Docker 容器使用压缩包解压安装的方式，软件安装于 `/opt/emqx` 目录中；
3. `data`、`log`、`plugins` 目录可以通过配置文件设置，建议将 `data` 目录挂载至高性能磁盘以获得更好的性能。但对于属于同一集群的节点， `data` 目录的配置应该相同。

|目录|描述|权限|目录文件|
|---|---|---|---|
|bin|存放可执行文件|读|`emqx` 和`emqx.cmd`：EMQX 的可执行文件，具体使用可以查看[命令行接口](https://www.emqx.io/docs/zh/v5.1/admin/cli.html)。|
|etc|存放配置文件|读|`emqx.conf`：EMQX 的主配置文件，默认包含常用的配置项。  <br>  <br>`emqx-example-en.conf`：EMQX 示例配置文件，包含所有可选的配置项。  <br>  <br>`acl.conf`：默认 ACL 规则。  <br>  <br>`vm.args`：Erlang 虚拟机的运行参数。  <br>  <br>`certs/`：X.509 的密钥和证书文件。这些文件被用于 EMQX 的 SSL/TLS 监听器；当要与和外部系统集成时，也可用于建立 SSL/TLS 连接。|
|data|存放 EMQX 的运行数据|写|`authz`：Dashboard 或 REST API 上传的 [基于文件进行授权](https://www.emqx.io/docs/zh/v5.1/access-control/authz/file.html) 规则内容。  <br>  <br>`certs`：Dashboard 或 REST API 上传的证书。  <br>  <br>`configs`：启动时生成的配置文件，或者从 Dashboard/REST API/CLI 进行功能设置时覆盖的配置文件。  <br>  <br>`mnesia`：内置数据库目录，用于存储自身运行数据，例如告警记录、客户端认证与权限数据、Dashboard 用户信息等数据，**一旦删除该目录，所有业务数据将丢失。**  <br>  <br>— 可包含以节点命名的子目录，如 `emqx@127.0.0.1`；如节点被重新命名，应手动将旧的目录删除或移走。  <br>  <br>— 可通过 `emqx_ctl mnesia` 命令查询 EMQX 中 Mnesia 数据库的系统信息，具体请查看 [管理命令 CLI](https://www.emqx.io/docs/zh/v5.1/admin/cli.html)。  <br>  <br>`patches`：用于存储热补丁 `.beam` 文件，用于补丁修复。  <br>  <br>`trace`: 在线日志追踪文件目录。  <br>  <br>  <br>在生产环境中，建议定期备份该文件夹下除 `trace` 之外的所有目录。|
|log|日志文件|读|`emqx.log.*`：EMQX 运行时产生的日志文件，具体请查看[日志](https://www.emqx.io/docs/zh/v5.1/observability/log.html)。  <br>  <br>`erlang.log.*`：当以 `emqx start` 方式后台启动 EMQX 时，控制台日志的副本文件。|
EMQX 的配置项存储在 `etc` 和 `data/configs` 目录下，二者的主要区别是 `etc` 目录存储**只读**的配置文件，用户通过 Dashboard 和 REST API 提交的配置将被保存到 `data/configs` 目录下，并支持在运行时进行热更新。

- `etc/emqx.conf`
- `data/configs/cluster.hocon`

EMQX 读取这些配置并将其合并转化为 Erlang 原生配置文件格式，以便在运行时应用这些配置。

### 升级
- 滚动升级
	- https://www.emqx.io/docs/zh/v5.1/deploy/rolling-upgrades.html#rpm-%E5%92%8C-deb
- 集群升级
	- https://www.emqx.io/docs/zh/v5.1/deploy/upgrade-cluster.html
- k8s升级
	- https://www.emqx.com/zh/blog/how-to-upgrade-emqx-in-kubernetes

## mqtt核心概念
- 服务端Broket
	- 本质就是mqtt的服务，基于erlang语言开发的信息桥
- 客户端
	- subscribe 订阅者
	- publish 发布者
	- clientId 客户端ID
- 主题
	- topic 信道？这里叫做主题
	-  [主题与通配符](https://www.emqx.com/zh/blog/advanced-features-of-mqtt-topics)订阅多个信道
- Qosd等级
	- QoS 0 最多交付一次，消息可能丢失；
	- QoS 1 至少交付一次，消息可以保证到达，但是可能重复；
	- QoS 2 只交付一次，消息保证到达，并且不会重复。
	- Session 会话：QoS 只是设计了消息可靠到达的理论机制，而会话则确保了 QoS 1、2 的协议流程得以真正实现。

### 使用paho.mqtt
topic主题：主题通过 `/` 来区分层级，类似于 URL 路径
```
chat/room/1
sensor/10/temperature
sensor/+/temperature
```
MQTT 主题支持以下两种通配符：`+` 和 `#`。
- `+`：表示单层通配符，例如 `a/+` 匹配 `a/x` 或 `a/y`。
- `#`：表示多层通配符，例如 `a/#` 匹配 `a/x`、`a/b/c/d`。
通配符只能用在订阅，不能用在发布。发布者必须是准确的，订阅者可以模糊。

<p style="color: red;">使用paho-mqtt作为我们的首选客户端，首选语言python</p>
```shell
pip install paho-mqtt 
```
https://eclipse.dev/paho/index.php?page=clients/python/docs/index.php
```python
Client
	- 构造函数/重新初始化
	- 选项功能
	- 连接/重新连接/断开连接
	- 网络环路
	- 出版
	- 订阅/取消订阅
	- 回调
	- 外部事件循环支持
	- 全局辅助函数
Publish（专用api）
	- 单身的
	- 多种的
Subscribe（专用api）
	- 简单的
	- 使用回调
```

选项功能
```python
from paho.mqtt import client as mqtt_client

handleClient = mqtt_client.Client(client_id="", clean_session=None, userdata=None,
                 protocol=MQTTv311, transport="tcp", reconnect_on_failure=True)

handleClient.connect(host, port=1883, keepalive=60, bind_address="", bind_port=0,
clean_start=MQTT_CLEAN_START_FIRST_ONLY, properties=None)

handleClient.loop(timeout=NONE)

handClient.publish(keepalive=60)

handClient.will_set(topic, "遗嘱消息", qos=1)
```


client_id: 
**如果客户端使用一个重复的 Client ID 连接至服务器，将会把已使用该 Client ID 连接成功的客户端踢下线。**

transport：
支持TCP 和 websocket
- 使用 1883 端口的 TCP 类型监听器
- 使用 8883 端口的 SSL/TLS 安全连接类型监听器
- 使用 8083 端口的 WebSocket 类型监听器
- 使用 8084 端口的 WebSocket 安全类型监听器
- 使用18083端口: web管理页面

userdata：
MQTT 协议可以通过用户名和密码来进行相关的认证和授权，但是如果此信息未加密，则用户名和密码将以明文方式传输。如果设置了用户名与密码认证，那么最好要使用 `mqtts` 或 `wss` 协议。

timeout:
连接超时时长，收到服务器连接确认前的等待时间，等待时间内未收到连接确认则为连接失败。

keepalive:
保活周期，是一个以秒为单位的时间间隔。客户端在无报文发送时，将按 Keep Alive 设定的值定时向服务端发送心跳报文，确保连接不被服务端断开。

在连接建立成功后，如果服务器没有在 Keep Alive 的 1.5 倍时间内收到来自客户端的任何包，则会认为和客户端之间的连接出现了问题，此时服务器便会断开和客户端的连接。

clean_session：
为 `false` 时表示创建一个[持久会话](https://www.emqx.com/zh/blog/mqtt-session)，在客户端断开连接时，会话仍然保持并保存离线消息，直到会话超时注销。为 `true` 时表示创建一个新的临时会话，在客户端断开时，会话自动销毁。
持久会话避免了客户端掉线重连后消息的丢失，并且免去了客户端连接后重复的订阅开销。这一功能在带宽小，网络不稳定的物联网场景中非常实用。

will_set:
遗嘱消息是 MQTT 为那些可能出现**意外断线**的设备提供的将**遗嘱**优雅地发送给其他客户端的能力。设置了遗嘱消息消息的 MQTT 客户端异常下线时，MQTT 服务器会发布该客户端设置的遗嘱消息。


#### 外部事件循环支持
当你需要手动执行socket中的event时，就需要使用这五个api，实现高级自定义事件循环。
了解即可。
##### socket()
首先你要获取socket对象。
```python
socket()
```
##### loop_read()
订阅等待。
```python
loop_read(max_packets=1)
```
##### loop_write()
发布等待。
```python
loop_write(max_packets=1)
```
##### loop_misc()
每隔几秒调用一次以处理消息重试和 ping。
```python
loop_misc()
```
##### want_write()
如果有数据等待写入，则返回 true，以允许将客户端与其他事件循环连接。
```python
want_write()
```

#### 全局辅助函数
判断订阅的topic字符串是否匹配到我想要的topic，返回true or false
主要是还是通配符和目标主题的匹配判断。
```python
topic_matches_sub(sub: str, topic: str)
```
状态代码映射状态内容。
```python
connack_string(connack_code: int) 
```
异常代码映射内容
```python
error_string(mqtt_errno: int)
```

#### 缓存信息
MQTT 客户端通常只能在在线状态下接收其它客户端发布的消息。如果客户端离线后重新上线，它将无法收到离线期间的消息。
但是，如果客户端连接时设置 Clean Session 为 false，并且使用相同的客户端 ID 再次上线，那么消息服务器将为客户端缓存一定数量的离线消息，并在它重新上线时发送给它。

在这里实现会话订阅缓存。
会话client.py
```python
#!/usr/bin/python

# -*- coding: utf-8 -*-

  
  

from paho.mqtt import client as mqtt_client

  

# 获取mqtt版本

from paho.mqtt.client import MQTTv311

  

# 获取额外传参属性 mqttv5

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

    #     self.host = host

    #     self.port = port

    #     self.client_id = client_id

    #     # 创建实例, v5版本没有clean_session 完全是由连接器定义

    #     self.handClient = mqtt_client.Client(client_id=self.client_id, protocol=MQTTv5, transport="tcp")

    #     self.handClient.on_message = self.on_message

  

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
```

会话发布者
会话publish.py
```python
#!/usr/bin/python

# -*- coding: utf-8 -*-

from paho.mqtt import client as mqtt_client

from paho.mqtt.client import MQTTv311

  
  

class Demo(object):

    def __init__(self, client_id, host, port):

        self.client_id = client_id

        self.host = host

        self.port = port

        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv311, transport="tcp")

        self.handClient.connect(host, port)

  

    def sendMessage(self, topic):

        for i in range(3):

            self.handClient.publish(topic, "保存会话", qos=1)

  
  

if __name__ == "__main__":

    # 客户端id

    client_id = "setGame"

    host = "localhost"

    port = 1883

    try:

        D = Demo(client_id, host, port)

        # 接受消息

        D.sendMessage("clean_session_false")

    except Exception as identifier:

        print(identifier)

    except KeyboardInterrupt:

        print("手动中断监听")

    else:

        print("结束")
```
Clean Session 是用来控制会话状态生命周期的标志位，为 `true` 时表示创建一个新的会话，在客户端断开连接时，会话将自动销毁。为 `false` 时表示创建一个持久会话，在客户端断开连接后会话仍然保持，直到会话超时注销。


支持会话配置。
http://localhost:18083/#/mqtt/session
![](readme.assets/Pasted%20image%2020230910111500.png)
mqtt3.1.1 会话缓存：只有Clean Session 值。
mqtt5.0 会话缓存：则将 Clean Session 拆分成了 Clean Start 与 Session Expiry Interval。
通过flags区分不同消息设置。




### 规则引擎
https://www.emqx.io/docs/zh/v5.1/data-integration/rules.html
规则引擎是 EMQX 内置基于 SQL 的数据处理组件，搭配[数据桥接](https://www.emqx.io/docs/zh/v5.1/data-integration/data-bridges.html)使用无需编写代码即可实现一站式的 IoT 数据提取、过滤、转换、存储与处理，以加速应用集成和业务创新。

http://localhost:18083/#/rules
可视化操作即可。
![](readme.assets/Pasted%20image%2020230911004425.png)


### 数据集成
https://www.emqx.io/docs/zh/v5.1/data-integration/data-bridges.html
EMQX 开源版中仅支持 MQTT 桥接 和 HTTP Server。

数据桥接是用来对接 EMQX 和外部数据系统的通道，比如 MySQL、MongoDB 等数据库， 或 Kafka，RabbitMQ 等消息中间件，或 HTTP 服务器等。

通过数据桥接，用户可以实时地将消息从 EMQX 发送到外部数据系统。如果使用双向数据桥接，用户还可以从外部数据系统拉取数据并发送到 EMQX 的某个主题。

这里我们需要借助 ekuiper 做mqtt数据桥接。
开源版支持的数据桥接。

![](readme.assets/Pasted%20image%2020230911004519.png)

#### 使用 ekuiper 作为mqtt数据桥接




### 管理员指南
https://www.emqx.io/docs/zh/v5.1/admin/admin-guide.html
- 配置文件参数和配置手册为您提供了配置文件基本信息，配置项以及详细的配置参考信息。
- [命令行接口](https://www.emqx.io/docs/zh/v5.1/admin/cli.html)介绍了 EMQX 支持的各类启动与管理命令。
- [EMQX Dashboard](https://www.emqx.io/docs/zh/v5.1/dashboard/introduction.html) 为您全面介绍 EMQX 内置的管理控制台，您将了解如何管理和监控 EMQX 集群并配置和使用所需的各项功能。
- [速率限制](https://www.emqx.io/docs/zh/v5.1/rate-limit/rate-limit.html)介绍了如何通过配置消息接入速度限制器避免系统过载，从而保证系统稳定。
- [日志及可观测性](https://www.emqx.io/docs/zh/v5.1/observability/overview.html)介绍了 EMQX 中的指标观测和监控功能，便于您进行系统监控和调试。
- [备份与恢复](https://www.emqx.io/docs/zh/v5.1/operations/backup-restore.html)指导您如何对 EMQX 数据进行备份和恢复。
- [插件与扩展](https://www.emqx.io/docs/zh/v5.1/extensions/introduction.html)帮助您通过开发插件来扩展 EMQX 的功能。



### 特殊消息

#### 保留消息
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-retained-message.html
数据持久化。不过是阉割版，只存储最新的一条。

发布者发布消息时，如果 Retained 标记被设置为 true，则该消息即是 MQTT 中的保留消息（Retained Message）。**MQTT 服务器会为每个主题存储最新一条保留消息，以方便消息发布后才上线的客户端在订阅主题时仍可以接收到该消息。**

与普通消息不同，保留消息可以保留在 MQTT 服务器中。任何新的订阅者订阅与该保留消息中的主题匹配的主题时，都会立即接收到该消息，即使这个消息是在它们订阅主题之前发布的。

这使订阅者在上线后可以立即获得数据更新，而不必等待发布者再次发布消息。在某种程度上，我们可以把保留消息当作是一个消息 “云盘” 来使用：随时上传消息到 “云盘”，然后在任意时刻从 “云盘” 获取消息。当然，这个 “云盘” 还有一个主题下只能存储一条最新的保留消息的限制。

```python

class Demo(object):
    def __init__(self, host, port, client_id) -> None:
        # 创建实例
        self.handClient = mqtt_client.Client(client_id=self.client_id, protocol=MQTTv311, transport="tcp")
        # 同步链接
        # self.handClient.connect(host, port)
        # 使用异步链接
        self.handClient.connect_async(host, port)
        # 开启异步事件
        self.handClient.loop_start()

    # 发送消息
    def sendMessage(self, topic):
        while True:
            message = f"保留消息{dt.today()}"
	        # retain 开启保留消息, 由发送者决定
            result = self.handClient.publish(topic, message, retain=True, qos=0)


```

(webSocket多了path，主要是请求地址url的路径  ws://broker.emqx.io:8083/mqtt)
![](readme.assets/Pasted%20image%2020230909200300.png)
保留消息配置。
http://localhost:18083/#/mqtt/retainer
![](readme.assets/Pasted%20image%2020230910111647.png)

emqx_learning/advance/保留消息server.py
```python
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
```




emqx_learning/advance/保留消息client.py
```python
#!/usr/bin/python

# -*- coding: utf-8 -*-

  
  

from paho.mqtt import client as mqtt_client

  

# 获取mqtt版本

from paho.mqtt.client import MQTTv311

  

# 全局辅助函数

from paho.mqtt.client import connack_string

import time

from datetime import datetime as dt

  
  

class Demo(object):

    def __init__(self, host, port, client_id) -> None:

        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv311, transport="tcp")

        self.handClient.connect_async(host, port)

        self.handClient.on_connect = self.on_connect

        self.handClient.loop_start()

  

    def on_connect(self, client, userdata, flags, rc):

        if rc == 0:

            print("链接状态", connack_string(rc))

        else:

            print("Failed to connect, return code %d\n", rc)

  

    # 发送消息

    def sendMessage(self, topic):

        while True:

            time.sleep(0.1)

            message = f"保留消息{dt.today()}"

            result = self.handClient.publish(topic, message, retain=True, qos=0)

  
  

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
```




#### 遗嘱消息
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-will-message.html
死信处理。

发布订阅模式的特性决定了，除了服务器以外没有客户端能够感知到某个客户端从通信网络中离开。而遗嘱消息则为连接意外断开的客户端提供了向其他客户端发出通知的能力。

客户端可以在连接时向服务器设置自己的遗嘱消息，服务器将在客户端异常断开后立即或延迟一段时间后发布这个遗嘱消息。而订阅了对应遗嘱主题的客户端，将收到这个遗嘱消息，并且采取相应的措施，例如更新该客户端的在线状态等等。

遗嘱消息是 [MQTT](https://www.emqx.com/zh/mqtt-guide) 为那些可能出现 **意外断线** 的设备提供的将 **遗嘱** 优雅地发送给第三方的能力。意外断线包括但不限于：

- 因网络故障或网络波动，设备在保持连接周期内未能通讯，连接被服务端关闭
- 设备意外掉电
- 设备尝试进行不被允许的操作而被服务端关闭连接，例如订阅自身权限以外的主题等

遗嘱订阅.py
```python
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
```

遗嘱发送.py
```python
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

        self.handClient = mqtt_client.Client(

            client_id=self.client_id,

            protocol=MQTTv311,

            transport="tcp",

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
```

#### 共享订阅
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-shared-subscription.html
过滤器和轮询方式。

共享订阅是 MQTT 5.0 协议引入的新特性，相当于是订阅端的[负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing)功能。

同非共享订阅一样，共享订阅包含一个主题过滤器和[订阅选项](https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options)，唯一的区别在于共享订阅的主题过滤器格式必须是 `$share/{ShareName}/{filter}` 这种形式。这几个的字段的含义分别是：

- `$share` 前缀表明这将是一个共享订阅
- `{ShareName}` 是一个不包含 "/", "+" 以及 "#" 的字符串。订阅会话通过使用相同的 `{ShareName}` 表示共享同一个订阅，匹配该订阅的消息每次只会发布给其中一个会话
- `{filter}` 即非共享订阅中的主题过滤器

虽然共享订阅使得订阅端能够[负载均衡](https://www.emqx.com/zh/blog/mqtt-broker-clustering-part-2-sticky-session-load-balancing)地消费消息，但 MQTT 协议并没有规定 Server 应当使用什么负载均衡策略。作为参考，EMQX 提供了 random, round_robin, sticky, hash 四种策略供用户自行选择。

- random: 在所有共享订阅会话中随机选择一个发送消息
- round_robin: 按照订阅顺序轮流选择
- sticky: 使用 random 策略随机选择一个订阅会话，持续使用至该会话取消订阅或断开连接再重复这一流程
- hash: 对发送者的 ClientID 进行 hash 操作，根据 hash 结果选择订阅会话

共享订阅。
http://localhost:18083/#/mqtt/general
![](readme.assets/Pasted%20image%2020230910181206.png)

##### ★坑
如果你想使用paho.mqtt进行共享订阅，记得发送者topic取$share/g/之后的路径。
支持# + 通用匹配符号。
```
订阅者们："$share/g/topic"
发送者："topic"
```

共享订阅发送端.py
```python
#!/usr/bin/python

# -*- coding: utf-8 -*-

  

from paho.mqtt import client as mqtt_client

from paho.mqtt.client import MQTTv5

import time

from paho import mqtt

  
  

class Demo(object):

    def __init__(self, host, port, client_id, publishTopic) -> None:

        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv5)

        self.handClient.connect_async(host, port)

        self.handClient.on_connect = self.on_connect

        self.publishTopic = publishTopic

  

    def on_connect(self, client, userdata, flags, reasonCode, properties):

        if reasonCode == 0:

            print("链接成功")

  

    def loop(self):

        while True:

            time.sleep(1)

            message = time.strftime("%X")

            self.handClient.publish(self.publishTopic, message)

  

    def run(self):

        self.handClient.loop_start()

        self.loop()

  

    def __del__(self):

        self.handClient.disconnect()

  
  

if __name__ == "__main__":

    # 客户端id

    client_id = "publish"

    host = "localhost"

    port = 1883

    publishTopic = "topic"

    try:

        D = Demo(client_id=client_id, host=host, port=port, publishTopic=publishTopic)

        D.run()

    except Exception as error:

        print(error)

    except KeyboardInterrupt:

        print("手动中断")

    else:

        print("结束")
```


共享订阅1.py / 共享订阅2.py
```python
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
```











#### $SYS主题
以 `$SYS/` 为前缀的主题被保留给服务器用来发布一些特定的消息，比如服务器的运行时间、客户端的上下线事件通知、当前连接的客户端数量等等。我们一般将这些主题称为系统主题，客户端可以订阅这些系统主题来获取服务器的有关信息。

系统主题，这里不能覆盖。
http://localhost:18083/#/mqtt/system-topic
|主题|说明|
|---|---|
|$SYS/brokers|EMQX 集群节点列表|
|$SYS/brokers/emqx@127.0.0.1/version|EMQX 版本|
|$SYS/brokers/emqx@127.0.0.1/uptime|EMQX 运行时间|
|$SYS/brokers/emqx@127.0.0.1/datetime|EMQX 系统时间|
|$SYS/brokers/emqx@127.0.0.1/sysdescr|EMQX 系统信息|
![](readme.assets/Pasted%20image%2020230910181149.png)
## 官方工具
随便用用吧。
https://www.emqx.io/docs/zh/v5.1/messaging/publish-and-subscribe.html#mqttx

## 排他订阅
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-exclusive-subscription.html
```python
client.subscriber("$exclusive/t/1") # 排他订阅，唯一订阅
client.publist("1") # 发布者
```

排它订阅是 EMQX 支持的 MQTT 扩展功能。排它订阅允许对主题进行互斥订阅，一个主题同一时刻仅被允许存在一个订阅者，在当前订阅者未取消订阅前，其他订阅者都将无法订阅对应主题。

要进行排它订阅，您需要为主题名称添加前缀，如以下表格中的示例：

|示例|前缀|真实主题名|
|---|---|---|
|$exclusive/t/1|$exclusive/|t/1|

当某个客户端 **A** 订阅 `$exclusive/t/1` 后，其他客户端再订阅 `$exclusive/t/1` 时都会失败，直到 **A** 取消了对 `$exclusive/t/1` 的订阅为止。

**注意**: 排它订阅必须使用 `$exclusive/` 前缀，在上面的示例中，其他客户端依然可以通过 `t/1` 成功进行订阅。

唯一订阅者。保证订阅者的独占topic。
![](readme.assets/Pasted%20image%2020230911001435.png)


## 自动订阅
用来做转发。
http://localhost:18083/#/auto-sub
自动订阅是 EMQX 支持的 MQTT 扩展功能。自动订阅能够给 EMQX 设置多个规则，在设备成功连接后按照规则为其订阅指定主题，不需要额外发起订阅。


在 EMQX 5.0 之前，改功能叫做代理订阅。

打开 EMQX Dashboard。在左侧导航菜单中，点击管理 -> 代理订阅。

在代理订阅页面，点击右上角的 + 添加按钮。

在弹出的对话框中，在主题文本框中输入测试主题 a/1。其他设置保持默认值。

主题: 输入客户端自动订阅的主题。
QoS: 指定主题的服务质量。选项：0、1 和 2。
No local: 选项：False 或 True。
保留发布: 指定是否保留使用指定主题发送的消息。选项：False 或 True。
保留处理: 选项：0、1 和 2。
auto-sub-dashboard
点击对话框中的添加按钮。自动订阅主题 a/1 创建成功。

auto-sub-dashboard-create
现在自动订阅功能已启用。新的订阅者一旦连接到代理服务器，将自动订阅主题 a/1

![](readme.assets/Pasted%20image%2020230911002052.png)

## 延迟订阅
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-delayed-publish.html
延迟发布是 EMQX 支持的 MQTT 扩展功能。当客户端使用特殊主题前缀 `$delayed/{DelayInteval}` 发布消息时，将触发延迟发布功能，可以实现按照用户配置的时间间隔延迟发布消息。

延迟发布主题的具体格式如下：

```
$delayed/{DelayInterval}/{TopicName}
```

- `$delayed`：使用 `$delay` 作为主题前缀的消息都将被视为需要延迟发布的消息。延迟间隔由下一主题层级中的内容决定。
- `{DelayInterval}`：指定该 MQTT 消息延迟发布的时间间隔，单位是秒，允许的最大间隔是 4294967 秒。如果 `{DelayInterval}` 无法被解析为一个整型数字，EMQX 将丢弃该消息，客户端不会收到任何信息。
- `{TopicName}`：MQTT 消息的主题名称。

例如:

- `$delayed/15/x/y`：15 秒后将 MQTT 消息发布到主题 `x/y`。
- `$delayed/60/a/b`：1 分钟后将 MQTT 消息发布到 `a/b`。
- `$delayed/3600/$SYS/topic`：1 小时后将 MQTT 消息发布到 `$SYS/topic`

![](readme.assets/Pasted%20image%2020230911001909.png)


## 主题重写
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-topic-rewrite.html
很多物联网设备不支持重新配置或升级，修改设备业务主题会非常困难。

主题重写功能可以帮助使这种业务升级变得更容易：通过给 EMQX 设置一套规则，它可以在订阅、发布时改变将原有主题重写为新的目标主题。

[保留消息](https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-retained-message.html) 和 [延迟发布](https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-delayed-publish.html) 也可以与主题重写结合使用。例如，当用户想使用延迟发布时，他们可以使用主题重写来将消息重定向到所需的主题。
http://localhost:18083/#/topic-rewrite
![](readme.assets/Pasted%20image%2020230911004236.png)
这个可视化操作即可，替换主题罢了。

## 通配符订阅
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-wildcard-subscription.html
批量订阅。
MQTT 主题名称是用于消息路由的 UTF-8 编码字符串。为了提供更大的灵活性，MQTT 支持分层主题命名空间。主题通常按层级分级，并使用斜杠 `/` 在级别之间进行分隔，例如 `chat/room/1`。[通配符订阅 (opens new window)](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html#_Topic_Names_and)允许客户端在主题名称中包含一个或多个通配符字符，通过主题过滤器匹配多个主题，从而实现一次订阅多个主题。本页介绍了 MQTT 中支持的两种类型的通配符的用法以及如何在 EMQX 中订阅包含通配符的主题。
**通配符只能用于订阅，不能用于发布。**

## 客户端SDK

这里我们选择python开发mqtt通讯协议。也用python当作代码示例。
- JavaScript
	- nodejs环境：mqtt 或者 WebSocket
	- browser环境：mqtt 或者 WebSocket
- Rust
	- Cargo.toml包管理添加依赖: paho-mqtt = { git = "https://github.com/eclipse/paho.mqtt.rust.git", branch = "master" }
- Python
	- paho-mqtt: https://github.com/eclipse/paho.mqtt.python
	- hbmqtt: https://github.com/beerfactory/hbmqtt
	- gmqtt: https://github.com/wialon/gmqtt
- Dart
	- mqtt_client: https://pub.dev/packages/mqtt_client
- 移动端
	- Flutter
	- Android
	- js跨平台框架

### keep alive 会话激活
https://www.emqx.com/zh/blog/mqtt-keep-alive
[MQTT 协议](https://mqtt.org/)是承载于 TCP 协议之上的，而 TCP 协议以连接为导向，在连接双方之间，提供稳定、有序的字节流功能。 但是，在部分情况下，TCP 可能出现半连接问题。所谓半连接，是指某一方的连接已经断开或者没有建立，而另外一方的连接却依然维持着。在这种情况下，半连接的一方可能会持续不断地向对端发送数据，而显然这些数据永远到达不了对端。为了避免半连接导致的通信黑洞，MQTT 协议提供了 **Keep Alive** 机制，使客户端和 [MQTT 服务器](https://www.emqx.io/zh)可以判定当前是否存在半连接问题，从而关闭对应连接。

只在链接时，存在心跳机制。
```python
class Demo(object):

    def __init__(self, host, port, client_id) -> None:

        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv5, transport="tcp")

        # 链接时，用户自定义的信息

        self.handClient.connect_async(host, port, properties=OPTIONS["properties"], keepalive=600)

        self.handClient.on_connect = self.on_connect

        self.handClient.loop_start()
```

### 用户信息

https://www.emqx.com/zh/blog/mqtt5-user-properties
用户属性（User Properties）其实是一种自定义属性，允许用户向 MQTT 消息添加自己的元数据，传输额外的自定义信息以扩充更多应用场景。

它由一个用户自定义的 UTF-8 的键/值对数组组成，并在消息属性字段中配置，只要不超过最大的消息大小，可以使用无限数量的用户属性来向 MQTT 消息添加元数据，并在发布者、[MQTT 服务器](https://www.emqx.io/zh)和订阅者之间传递信息。

如果你熟悉 HTTP 协议的话，该功能与 HTTP 的 Header 的概念非常类似。用户属性有效地允许用户扩展 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide)，并且可以出现在所有消息和响应中。因为用户属性是由用户定义的，它们只对该用户的实现有意义。

```python
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

        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv5, transport="tcp")

        # 链接时，用户自定义的信息

        self.handClient.connect_async(host, port, properties=OPTIONS["properties"])

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
```


### 认证权限
https://www.emqx.io/docs/zh/v5.1/access-control/security-guide.html

#### 访问控制
介绍了关于认证和授权的相关功能设定和操作以及如何设置黑名单。

##### 用户密码
```python
class Demo(object):

    def __init__(self, host, port, client_id) -> None:

        self.handClient = mqtt_client.Client(client_id=client_id, protocol=MQTTv5, transport="tcp", userdata={"username": "leroy", "password": "password"})

        # 链接时，用户自定义的信息

        self.handClient.connect_async(host, port, properties=OPTIONS["properties"], keepalive=600)

        self.handClient.on_connect = self.on_connect

        self.handClient.loop_start()
```


###### api认证
https://www.emqx.io/docs/zh/v5.0/access-control/authn/user_management.html
前端的日常认证。

##### 增强认证
https://www.emqx.io/docs/zh/v5.0/access-control/authn/scram.html
如果求简单，则我推荐这种认证方式。

##### JWT 认证
https://www.emqx.io/docs/zh/v5.0/access-control/authn/jwt.html
token 比较主流。需要自行集成一下。

#### 通道加密
端对端加密通信，包括如何启用 SSL/TLS 连接和 PSK 验证、如何进行获取 SSL/TLS 证书。
这里就是openssl地方。
```python
tls_set(ca_certs=None, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLS, ciphers=None)
```
```python
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.tls_set(ca_certs="ca_certificate.pem", certfile="client_certificate.pem", keyfile="client_key.pem")
```
这是一个更传统的方法，用于配置 TLS/SSL 连接的参数。
ca_certs：指定 CA 根证书的路径。
certfile：指定客户端证书的路径。
keyfile：指定客户端私钥的路径。
cert_reqs：控制是否要求服务器验证客户端证书，可以是 ssl.CERT_NONE、ssl.CERT_OPTIONAL 或 ssl.CERT_REQUIRED。
tls_version：指定 TLS 协议版本。
ciphers：指定可用的加密算法。


```python
import paho.mqtt.client as mqtt
import ssl

client = mqtt.Client()
context = ssl.SSLContext(ssl.PROTOCOL_TLS)
context.load_cert_chain(certfile="client_certificate.pem", keyfile="client_key.pem")
client.tls_set_context(context)
```
context 是一个可选的 SSLContext 对象，用于配置 TLS/SSL 连接的参数。如果未提供 context，则会使用默认的 SSLContext。
通常，您可以通过创建自定义的 SSLContext 对象并将其传递给 tls_set_context() 来配置 TLS 连接的各种参数，例如证书、密钥、CA 根证书等。

```python
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.tls_insecure_set(True)  # 禁用服务器证书验证
client.tls_insecure_set(False)  # 启动服务器证书验证
```
flag 是一个布尔值，用于控制是否禁用对服务器证书的验证。
如果将 flag 设置为 True，则表示禁用服务器证书验证，客户端将接受来自服务器的任何证书，包括自签名证书，而不进行验证。
如果将 flag 设置为 False，则表示启用服务器证书验证，客户端将验证服务器证书的有效性。

### 客户端自定义报文长度
https://www.emqx.com/zh/blog/best-practices-of-maximum-packet-size-in-mqtt
MQTT 报文的理论最大长度为 268435456 字节，也就是 256 MB。但显然，不仅仅是资源受限的客户端，一些作为边缘网关运行的 MQTT 服务端，可能也无法处理这一长度的报文。

考虑到不同客户端对报文的处理能力可能有着较大差异，发送过大的报文不仅可能影响对端的正常业务处理，甚至可能直接压垮对端。所以，我们需要使用 Maximum Packet Size 属性来协商客户端和服务端各自能够处理的最大报文长度。

客户端首先在 CONNECT 报文中通过 Maximum Packet Size 来指定允许服务端给自己发送的报文的最大长度，而服务端则会在 CONNACK 报文中同样通过 Maximum Packet Size 来指定允许客户端给自己发送的报文的最大长度。
![](readme.assets/Pasted%20image%2020230911002247.png)

### 错误代码
看看就好。不常用。
https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack
|**Reason Code**|**Name**|**Packets**|**Details**|
|---|---|---|---|
|0x00|Success|CONNACK, PUBACK, PUBREC, PUBREL, PUBCOMP, UNSUBACK, AUTH|这个 Reason Code 可以用在所有存在 Reason Code 的报文中，例如 CONNACK、DISCONNECT 报文等等。它通常用于表示成功，比如连接成功、取消订阅成功、消息接收成功和认证成功等等。|
|0x00|Normal disconnection|DISCONNECT|在 DISCONNECT 报文中，0 则表示连接正常断开，这种情况下遗嘱消息不会被发布。|
|0x00|Granted QoS 0|SUBACK|0，1，2 在 SUBACK 这个订阅确认报文中，用来指示订阅结果，它们都表示订阅成功，同时向订阅端指示最终被授予的最大 QoS 等级，0，1，2 正好对应了三个 QoS 等级。 这是因为服务端最终授予的最大 QoS 等级，可能小于订阅时请求的最大 QoS 等级。比如订阅时请求的最大 QoS 等级是 2，但服务端最高仅支持 QoS 1 等等。|
|0x01|Granted QoS 1|SUBACK|-|
|0x02|Granted QoS 2|SUBACK|-|
|0x04|Disconnect with Will Message|DISCONNECT|仅用于 DISCONNECT 报文，适用于客户端希望正常断开连接但服务端仍然需要发布遗嘱消息的情况，比如客户端希望会话过期时可以对外发出通知。|
|0x10|No matching subscribers|PUBACK, PUBREC|这个 Reason Code 用于向发送方指示，消息已经收到，但是当前没有匹配的订阅者，所以只有服务端可以使用这个 Reason Code。我们可以通过收到 Reason Code 为 0x10 的响应报文得知当前没有人会收到自己的消息，但是不能通过没有收到 Reason Code 为 0x10 的响应报文来假定所有人都会收到自己的消息，除非最多只会存在一个订阅者。但需要注意，没有匹配的订阅者时使用 0x10 替代 0x00，并不是一个必须实现的行为，这取决于服务端的具体实现。|
|0x11|No subscription existed|UNSUBACK|仅用于 UNSUBACK 报文，表示取消订阅时没有发现匹配的订阅。|
|0x18|Continue authentication|AUTH|仅用于 AUTH 报文，表示继续认证，通过这个 Reason Code，客户端和服务端之间可以进行任意次数的 AUTH 报文交换，以满足不同的认证方法的需要。|
|0x19|Re-authenticate|AUTH|仅用于 AUTH 报文，在增强认证成功后客户端可以随时通过发送 Reason Code 为 0x19 的 AUTH 报文发起重新认证。重新认证期间，其他报文收发会正常继续，如果重新认证失败，连接就会被关闭。|
|0x80|Unspecified error|CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT|表示未指明的错误。当一方不希望向另一方透露错误的具体原因，或者协议规范中没有能够匹配当前情况的 Reason Code 时，那么它可以在报文中使用这个 Reason Code。|
|0x81|Malformed Packet|CONNACK, DISCONNECT|当收到了无法根据协议规范正确解析的控制报文时，接收方需要发送 Reason Code 为 0x81 的 DISCONNECT 报文来断开连接。如果是 CONNECT 报文存在问题，那么服务端应该使用 CONNACK 报文。当控制报文中出现固定报头中的保留位没有按照协议要求置 0、QoS 被指定为 3、UTF-8 字符串中包含了一个空字符等等这些情况时，都将被认为是一个畸形的报文。|
|0x82|Protocol Error|CONNACK, DISCONNECT|在控制报文被按照协议规范解析后检测到的错误，比如包含协议不允许的数据，行为与协议要求不符等等，都会被认为是协议错误。接收方需要发送 Reason Code 为 0x81 的 DISCONNECT 报文来断开连接。如果是 CONNECT 报文存在问题，那么服务端应该使用 CONNACK 报文。常见的协议错误包括，客户端在一个连接内发送了两个 CONNECT 报文、一个报文中包含了多个相同的属性，以及某个属性被设置成了一个协议不允许的值等等。但是当我们有其他更具体的 Reason Code 时，就不会使用 0x81 (Malformed Packet) 或者 0x82 (Protocol Error) 了。例如，服务端已经声明自己不支持保留消息，但客户端仍然向服务端发送保留消息，这本质上也属于协议错误，但我们会选择使用 0x9A (Retain not supported) 这个能够更清楚指明错误原因的 Reason Code。|
|0x83|Implementation specific error|CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT|报文有效，但是不被当前接收方的实现所接受。|
|0x84|Unsupported Protocol Version|CONNACK|仅用于 CONNACK 报文。对于支持了 MQTT 5.0 的服务端来说，如果不支持客户端当前使用的 MQTT 协议版本，或者客户端指定了一个错误的协议版本或协议名。例如，客户端将协议版本设置为 6，那么服务端可以发送 Reason Code 为 0x84 的 CONNACK 报文，表示不支持该协议版本并且表明自己 MQTT 服务端的身份，然后关闭网络连接。当然服务端也可以选择直接关闭网络连接，因为使用 MQTT 3.1 或 3.1.1 的 MQTT 客户端可能并不能理解 0x84 这个 Reason Code 的含义。这两个版本都是在 CONNACK 报文使用 0x01 来表示不支持客户端指定的协议版本。|
|0x85|Client Identifier not valid|CONNACK|仅用于 CONNACK 报文，表示 Client ID 是有效的字符串，但是服务端不允许。可能的情形有 Clean Start 为 0 但 Client ID 为空、或者 Client ID 超出了服务端允许的最大长度等等。|
|0x86|Bad User Name or Password|CONNACK|仅用于 CONNACK 报文，表示客户端使用了错误的用户名或密码，这也意味着客户端将被拒绝连接。|
|0x87|Not authorized|CONNACK, PUBACK, PUBREC, SUBACK, UNSUBACK, DISCONNECT|当客户端使用 Token 认证或者增强认证时，使用 0x87 来表示客户端没有被授权连接会比 0x86 更加合适。当客户端进行发布、订阅等操作时，如果没有通过服务端的授权检查，那么服务端也可以在 PUBACK 等应答报文中指定 0x87 这个 Reason Code 来指示授权结果。|
|0x88|Server unavailable|CONNACK|仅用于 CONNACK 报文，向客户端指示当前服务端不可用。比如当前服务端认证服务异常无法接入新客户端等等。|
|0x89|Server busy|CONNACK, DISCONNECT|向客户端指示服务端正忙，请稍后再试。|
|0x8A|Banned|CONNACK|仅用于 CONNACK 报文，表示客户端被禁止登录。例如服务端检测到客户端的异常连接行为，所以将这个客户端的 Client ID 或者 IP 地址加入到了黑名单列表中，又或者是后台管理人员手动封禁了这个客户端，当然以上这些通常需要视服务端的具体实现而定。|
|0x8B|Server shutting down|DISCONNECT|仅用于 DISCONNECT 报文，并且只有服务端可以使用。如果服务端正在或即将关闭，它可以通过主动发送 Reason Code 为 0x8B 的 DISCONNECT 报文的方式告知客户端连接因为服务端正在关闭而被终止。这可以帮助客户端避免在连接关闭后继续向此服务端发起连接请求。|
|0x8C|Bad authentication method|CONNACK, DISCONNECT|当服务端不支持客户端指定的增强认证方法，或者客户端在重新认证时使用了和之前认证不同的认证方法时，那么服务端就会发送 Reason Code 为 0x8C 的 CONNACK 或者 DISCONNECT 报文。|
|0x8D|Keep Alive timeout|DISCONNECT|仅用于 DISCONNECT 报文，并且只有服务端可以使用。如果客户端没能在 1.5 倍的 Keep Alive 时间内保持通信，服务端将会发送 Reason Code 为 0x8D 的 DISCONNECT 报文然后关闭网络连接。|
|0x8E|Session taken over|DISCONNECT|仅用于 DISCONNECT 报文，并且只有服务端可以使用。当客户端连接到服务端时，如果服务端中已经存在使用相同 Client ID 的客户端连接，那么服务端就会向原有的客户端发送 Reason Code 为 0x8E 的 DISCONNECT 报文，表示会话被新的客户端连接接管，然后关闭原有的网络连接。不管新的客户端连接中的 Clean Start 是 0 还是 1，服务端都会使用这个 Reason Code 向原有客户端指示会话被接管。|
|0x8F|Topic Filter invalid|SUBACK, UNSUBACK, DISCONNECT|主题过滤器的格式正确，但是不被服务端接受。比如主题过滤器的层级超过了服务端允许的最大数量限制，或者主题过滤器中包含了空格等不被当前服务端接受的字符。|
|0x90|Topic Name invalid|CONNACK, PUBACK, PUBREC, DISCONNECT|主题名的格式正确，但是不被客户端或服务端接受。|
|0x91|Packet Identifier in use|PUBACK, PUBREC, SUBACK, UNSUBACK|表示收到报文中的 Packet ID 正在被使用，例如发送方发送了一个 Packet ID 为 100 的 QoS 1 消息，但是接收方认为当前有一个使用相同 Packet ID 的 QoS 2 消息还没有按成它的报文流程。这通常意味着当前客户端和服务端之前的会话状态不匹配，可能需要通过设置 Clean Start 为 1 重新连接来重置会话状态。|
|0x92|Packet Identifier not found|PUBREL, PUBCOMP|表示未找到对应的 Packet ID，这只会在 QoS 2 的报文交互流程中发生。比如当接收方回复 PUBREC 报文时，发送方未找到使用相同 Packet ID 的等待确认的 PUBLISH 报文，或者当发送方发送 PUBREL 报文时，接收方未找到使用相同 Packet ID 的 PUBREC 报文。这通常意味着当前客户端和服务端之间的会话状态不匹配，可能需要通过设置 Clean Start 为 1 重新连接来重置会话状态。|
|0x93|Receive Maximum exceeded|DISCONNECT|仅用于 DISCONNECT 报文，表示超出了接收最大值。MQTT 5.0 增加了流控机制，客户端和服务端在连接时通过 Receive Maximum 属性约定它们愿意并发处理的可靠消息数（QoS > 0）。所以一旦发送方发送的没有完成确认的消息超过了这一数量限制，接收方就会发送 Reason Code 为 0x93 的 DISCONNECT 报文然后关闭网络连接。|
|0x94|Topic Alias invalid|DISCONNECT|仅用于 DISCONNECT 报文，表示主题别名不合法。如果 PUBLISH 报文中的主题别名值为 0 或者大于连接时约定的最大主题别名，接收方会将此视为协议错误，它将发送 Reason Code 为 0x94 的 DISCONNECT 报文然后关闭网络连接。|
|0x95|Packet too large|CONNACK, DISCONNECT|用于表示报文超过了最大允许长度。客户端和服务端各自允许的最大报文长度，可以在 CONNECT 和 CONNACK 报文中通过 Maximum Packet Size 属性约定。当一方发送了过大的报文，那么另一方将发送 Reason Code 为 0x95 的 DISCONNECT 报文，然后关闭网络连接。由于客户端可以在连接时设置遗嘱消息，因此 CONNECT 报文也有可能超过服务端能够处理的最大报文长度限制，此时服务端需要在 CONNACK 报文中使用这个 Reason Code。|
|0x96|Message rate too high|DISCONNECT|仅用于 DISCONNECT 报文，表示超过了允许的最大消息发布速率。需要注意它与 Quota exceeded 的区别，Message rate 限制消息的发布速率，比如每秒最高可发布多少消息，Quota 限制的是资源的配额，比如客户端每天可以发布的消息数量，但客户端可能在一小时内耗尽它的配额。|
|0x97|Quota exceeded|CONNACK, PUBACK, PUBREC, SUBACK, DISCONNECT|用于表示超出了配额限制。服务端可能会对发布端的发送配额进行限制，比如每天最多为其转发 1000 条消息。当发布端的配额耗尽，服务端就会在 PUBACK 等确认报文中使用这个 Reason Code 提醒对方。另一方面，服务端还可能限制客户端的连接数量和订阅数量，当超出这一限制时，服务端就会通过 CONNACK 或者 SUBACK 报文向客户端指示当前超出了配额。一些严格的客户端和服务端，在发现对端超出配额时，可能会选择发送 DISCONNECT 报文然后关闭连接。|
|0x98|Administrative action|DISCONNECT|仅用于 DISCONNECT 报文，向客户端指示连接因为管理操作而被关闭，例如运维人员在后台踢除了这个客户端连接等等。|
|0x99|Payload format invalid|CONNACK, PUBACK, PUBREC, DISCONNECT|当消息中包含 Payload Format Indicator 属性时，接收方可以检查消息中 Payload 的格式与该属性是否匹配。如果不匹配，接收方需要发送 Reason Code 为 0x99 的确认报文。一些严格的客户端或者服务器，可能会直接发送 DISCONNECT 报文然后关闭网络连接。如果是 CONNECT 报文中的遗嘱消息存在问题，服务端将发送 Reason Code 为 0x99 的 CONNACK 报文然后关闭网络连接。|
|0x9A|Retain not supported|CONNACK, DISCONNECT|当服务端不支持保留消息，但是客户端发送了保留消息时，服务端就会向它发送 Reason Code 为 0x9A 的 DISCONNECT 报文然后关闭网络连接。由于客户端还可以在连接时将遗嘱消息设置为保留消息，所以服务端也可能在 CONNACK 报文中使用这个 Reason Code。|
|0x9B|QoS not supported|CONNACK, DISCONNECT|用于表示不支持当前的 QoS 等级。如果客户端在消息（包括遗嘱消息）中指定的 QoS 大于服务端支持的最大 QoS，服务端将会发送 Reason Code 为 0x9B 的 DISCONNECT 或者 CONNACK 报文然后关闭网络连接。在大部份情况下，这个 Reason Code 都是由服务端使用。但是在客户端收到不是来自订阅的消息，并且消息的 QoS 大于它支持的最大 QoS 时，它也会发送 Reason Code 为 0x9B 的 DISCONNECT 报文然后关闭网络连接。这种情况通常意味着服务端的实现可能存在问题。|
|0x9C|Use another server|CONNACK, DISCONNECT|服务端在 CONNACK 或者 DISCONNECT 报文中通过这个 Reason Code 告知客户端应该临时切换到另一个服务端。如果另一个服务端不是客户端已知的，那么这个 Reason Code 还需要配合 Server Reference 属性一起使用，以告知客户端新的服务端的地址。|
|0x9D|Server moved|CONNACK, DISCONNECT|服务端在 CONNACK 或者 DISCONNECT 报文中通过这个 Reason Code 告知客户端应该永久切换到另一个服务端。如果另一个服务端不是客户端已知的，那么这个 Reason Code 还需要配合 Server Reference 属性一起使用，以告知客户端新的服务端的地址。|
|0x9E|Shared Subscriptions not supported|SUBACK, DISCONNECT|当服务端不支持共享订阅，但是客户端尝试建立共享订阅时，服务端可以发送 Reason Code 为 0x9E 的 SUBACK 报文拒绝这次订阅请求，也可以直接发送 Reason Code 为 0x9E 的 DISCONNECT 报文然后关闭网络连接。|
|0x9F|Connection rate exceeded|CONNACK, DISCONNECT|用于表示客户端已超过连接速率限制。服务端可以对客户端的连接速率做出限制，客户端连接过快时，服务端可以发送 Reason Code 为 0x9F 的 CONNACK 报文来拒绝新的连接。当然这并不是绝对的情况，考虑到不是所有的客户端都会等待一段时间再重新发起连接，一些服务端实现可能会选择暂时挂起连接而不是返回 CONNACK。|
|0xA0|Maximum connect time|DISCONNECT|仅用于 DISCONNECT 报文，并且只有服务端可以使用。出于安全性的考虑，服务端可以限制单次授权中客户端的最大连接时间，比如在使用 JWT 认证时，客户端连接不应在 JWT 过期后继续保持。这种情况下，服务端可以发送 Reason Code 为 0xA0 的 DISCONNECT 报文，向客户端指示连接因为超过授权的最大连接时间而被关闭。客户端可以在收到包含这个 Reason Code 的 DISCONNECT 报文后，重新获取认证凭据然后再次请求连接。|
|0xA1|Subscription Identifiers not supported|SUBACK, DISCONNECT|当服务端不支持订阅标识符，但是客户端的订阅请求中包含了订阅标识符时，服务端可以发送 Reason Code 为 0xA1 的 SUBACK 报文拒绝这次订阅请求，也可以直接发送 Reason Code 为 0xA1 的 DISCONNECT 报文然后关闭网络连接。|
|0xA2|Wildcard Subscriptions not supported|SUBACK, DISCONNECT|当服务端不支持通配符订阅，但是客户端的订阅请求中包含了主题通配符时，服务端可以发送 Reason Code 为 0xA2 的 SUBACK 报文拒绝这次订阅请求，也可以直接发送 Reason Code 为 0xA2 的 DISCONNECT 报文然后关闭网络连接。|


### 订阅标识符
https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options
MQTT 允许服务端为这些重叠的订阅分别发送一次消息，也允许服务端为这些重叠的订阅只发送一条消息，前者意味着客户端将收到多条重复的消息。

而不管是前者还是后者，客户端都不能确定消息来自于哪个或者哪些订阅。因为即使客户端发现某条消息同时与自己的两个订阅相匹配，也不能保证在服务端向自己转发这条消息时，这两个订阅是否都已经成功创建了。所以，客户端无法为消息触发正确的回调。

为了解决这个问题，MQTT 5.0 引入了订阅标识符。它的用法非常简单，客户端可以在订阅时指定一个订阅标识符，服务端则需要存储该订阅与订阅标识符的映射关系。当有匹配该订阅的 PUBLISH 报文要转发给此客户端时，服务端会将与该订阅关联的订阅标识符随 PUBLISH 报文一并返回给客户端。

```python
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
```


### 下一代协议
https://www.emqx.io/docs/zh/v5.1/mqtt-over-quic/getting-started.html
#### QUIC
https://www.emqx.io/docs/zh/v5.1/mqtt-over-quic/introduction.html
MQTT 协议广泛用于物联网和车联网的消息服务应用开发。MQTT 基于传输协议工作，传输协议提供可靠、有序和无丢失字节流的双向通信。这种可靠的传输协议可以确保消息的准确传递和按发送顺序接收。在传统物联网场景中，MQTT 协议主要基于 TCP 的协议进行消息的传输，如原始 TCP、TCP/TLS（用于安全性）和 WebSocket（用于 Web 浏览器适配）。然而，在某些场景下，复杂的网络条件可能会限制 MQTT 在这些场景下的应用，例如高延迟、高丢包率和信号弱或不稳定的网络。

为了克服 MQTT 基于 TCP 传输的局限性，EMQX 5.0 开创性地引入了一种新协议 MQTT over QUIC，使 MQTT 客户端和 EMQX 可以通过 Quick UDP Internet Connections (QUIC) 进行通信。该协议提供了与现有 MQTT 协议相同的功能，但具有 QUIC 的额外优势。


#### 多协议网关
https://www.emqx.io/docs/zh/v5.1/gateway/gateway.html
网关（Gateway）负责处理所有非 MQTT 协议的连接、认证和消息收发，并为其提供统一的用户层接口和概念。

在 EMQX 5.0 之前，非 MQTT 协议的接入分别由不同的接入插件实现（例如，`emqx_lwm2m` 插件用于处理 LwM2M 的协议接入） 这些插件之间存在设计和实现上差异，这导致使用这些接入插件会很难以理解。 在 5.0 中，EMQX 为其定义了统一的概念和操作模型以降低使用难度。

常用的网关快速开始：

- [Stomp](https://www.emqx.io/docs/zh/v5.1/gateway/stomp.html)
- [MQTT-SN](https://www.emqx.io/docs/zh/v5.1/gateway/mqttsn.html)
- [CoAP](https://www.emqx.io/docs/zh/v5.1/gateway/coap.html)
- [LwM2M](https://www.emqx.io/docs/zh/v5.1/gateway/lwm2m.html)
- [Exproto](https://www.emqx.io/docs/zh/v5.1/gateway/exproto.html)
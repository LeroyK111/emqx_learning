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
docker run -d --name emqx -p 1883:1883 -p 8083:8083 -p 8084:8084 -p 8883:8883 -p 18083:18083 emqx/emqx:latest
```

控制台地址： http://localhost:18083/
​默认用户名，密码：admin，public

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

### 规则引擎
https://www.emqx.io/docs/zh/v5.1/data-integration/rules.html
规则引擎是 EMQX 内置基于 SQL 的数据处理组件，搭配[数据桥接](https://www.emqx.io/docs/zh/v5.1/data-integration/data-bridges.html)使用无需编写代码即可实现一站式的 IoT 数据提取、过滤、转换、存储与处理，以加速应用集成和业务创新。

### 数据集成
https://www.emqx.io/docs/zh/v5.1/data-integration/data-bridges.html
EMQX 开源版中仅支持 MQTT 桥接 和 HTTP Server。

数据桥接是用来对接 EMQX 和外部数据系统的通道，比如 MySQL、MongoDB 等数据库， 或 Kafka，RabbitMQ 等消息中间件，或 HTTP 服务器等。

通过数据桥接，用户可以实时地将消息从 EMQX 发送到外部数据系统。如果使用双向数据桥接，用户还可以从外部数据系统拉取数据并发送到 EMQX 的某个主题。

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

#### 遗嘱消息
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-will-message.html
死信处理。

发布订阅模式的特性决定了，除了服务器以外没有客户端能够感知到某个客户端从通信网络中离开。而遗嘱消息则为连接意外断开的客户端提供了向其他客户端发出通知的能力。

客户端可以在连接时向服务器设置自己的遗嘱消息，服务器将在客户端异常断开后立即或延迟一段时间后发布这个遗嘱消息。而订阅了对应遗嘱主题的客户端，将收到这个遗嘱消息，并且采取相应的措施，例如更新该客户端的在线状态等等。

遗嘱消息是 [MQTT](https://www.emqx.com/zh/mqtt-guide) 为那些可能出现 **意外断线** 的设备提供的将 **遗嘱** 优雅地发送给第三方的能力。意外断线包括但不限于：

- 因网络故障或网络波动，设备在保持连接周期内未能通讯，连接被服务端关闭
- 设备意外掉电
- 设备尝试进行不被允许的操作而被服务端关闭连接，例如订阅自身权限以外的主题等


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

#### $SYS主题
以 `$SYS/` 为前缀的主题被保留给服务器用来发布一些特定的消息，比如服务器的运行时间、客户端的上下线事件通知、当前连接的客户端数量等等。我们一般将这些主题称为系统主题，客户端可以订阅这些系统主题来获取服务器的有关信息。

## 官方工具
随便用用吧。
https://www.emqx.io/docs/zh/v5.1/messaging/publish-and-subscribe.html#mqttx

## 排他订阅
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-exclusive-subscription.html
唯一订阅者。保证订阅者的独占topic。

## 自动订阅
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-auto-subscription.html
自动订阅是 EMQX 支持的 MQTT 扩展功能。自动订阅能够给 EMQX 设置多个规则，在设备成功连接后按照规则为其订阅指定主题，不需要额外发起订阅。

在 EMQX 5.0 之前，改功能叫做代理订阅。

## 主题重写
https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-topic-rewrite.html
很多物联网设备不支持重新配置或升级，修改设备业务主题会非常困难。

主题重写功能可以帮助使这种业务升级变得更容易：通过给 EMQX 设置一套规则，它可以在订阅、发布时改变将原有主题重写为新的目标主题。

[保留消息](https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-retained-message.html) 和 [延迟发布](https://www.emqx.io/docs/zh/v5.1/messaging/mqtt-delayed-publish.html) 也可以与主题重写结合使用。例如，当用户想使用延迟发布时，他们可以使用主题重写来将消息重定向到所需的主题。

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

### 用户信息

https://www.emqx.com/zh/blog/mqtt5-user-properties
用户属性（User Properties）其实是一种自定义属性，允许用户向 MQTT 消息添加自己的元数据，传输额外的自定义信息以扩充更多应用场景。

它由一个用户自定义的 UTF-8 的键/值对数组组成，并在消息属性字段中配置，只要不超过最大的消息大小，可以使用无限数量的用户属性来向 MQTT 消息添加元数据，并在发布者、[MQTT 服务器](https://www.emqx.io/zh)和订阅者之间传递信息。

如果你熟悉 HTTP 协议的话，该功能与 HTTP 的 Header 的概念非常类似。用户属性有效地允许用户扩展 [MQTT 协议](https://www.emqx.com/zh/mqtt-guide)，并且可以出现在所有消息和响应中。因为用户属性是由用户定义的，它们只对该用户的实现有意义。

### 认证权限
https://www.emqx.io/docs/zh/v5.1/access-control/security-guide.html

#### 访问控制
介绍了关于认证和授权的相关功能设定和操作以及如何设置黑名单。

##### 用户密码

###### api认证


##### 增强认证

##### JWT 认证


#### 通道加密
端对端加密通信，包括如何启用 SSL/TLS 连接和 PSK 验证、如何进行获取 SSL/TLS 证书。


### 客户端自定义报文长度
https://www.emqx.com/zh/blog/best-practices-of-maximum-packet-size-in-mqtt
MQTT 报文的理论最大长度为 268435456 字节，也就是 256 MB。但显然，不仅仅是资源受限的客户端，一些作为边缘网关运行的 MQTT 服务端，可能也无法处理这一长度的报文。

考虑到不同客户端对报文的处理能力可能有着较大差异，发送过大的报文不仅可能影响对端的正常业务处理，甚至可能直接压垮对端。所以，我们需要使用 Maximum Packet Size 属性来协商客户端和服务端各自能够处理的最大报文长度。

客户端首先在 CONNECT 报文中通过 Maximum Packet Size 来指定允许服务端给自己发送的报文的最大长度，而服务端则会在 CONNACK 报文中同样通过 Maximum Packet Size 来指定允许客户端给自己发送的报文的最大长度。


### 错误代码
看看就好。不常用。
https://www.emqx.com/zh/blog/mqtt5-new-features-reason-code-and-ack



### 订阅标识符
https://www.emqx.com/zh/blog/subscription-identifier-and-subscription-options
MQTT 允许服务端为这些重叠的订阅分别发送一次消息，也允许服务端为这些重叠的订阅只发送一条消息，前者意味着客户端将收到多条重复的消息。

而不管是前者还是后者，客户端都不能确定消息来自于哪个或者哪些订阅。因为即使客户端发现某条消息同时与自己的两个订阅相匹配，也不能保证在服务端向自己转发这条消息时，这两个订阅是否都已经成功创建了。所以，客户端无法为消息触发正确的回调。

为了解决这个问题，MQTT 5.0 引入了订阅标识符。它的用法非常简单，客户端可以在订阅时指定一个订阅标识符，服务端则需要存储该订阅与订阅标识符的映射关系。当有匹配该订阅的 PUBLISH 报文要转发给此客户端时，服务端会将与该订阅关联的订阅标识符随 PUBLISH 报文一并返回给客户端。


### 下一代协议
https://www.emqx.io/docs/zh/v5.1/mqtt-over-quic/advanced-feature.html

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
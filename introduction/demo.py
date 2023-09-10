import paho.mqtt.client as mqtt


def handle_yo(client, userdata, msg):
    print(f"Yo: {msg.payload}")


def handle_hi(client, userdata, msg):
    print(f"Hi: {msg.payload}")


def on_connect(client, userdata, flags, rc):
    # The subscription topic is a shared topic
    client.subscribe("$share/group/base/#")
    print("Subscribed")


c = mqtt.Client()
c.on_connect = on_connect

# Message callbacks drop the `$share/group` portion
c.message_callback_add("base/+/yo", handle_yo)
c.message_callback_add("base/+/hi", handle_hi)
c.connect("localhost", 1883)

c.loop_forever()

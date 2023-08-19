import paho.mqtt.client as mqtt

# Define broker and connection settings
broker_address = "broker.emqx.io"
port = 1883
username = "admin"
password = "admin"

# Callback function when a message is received on subscribed topics
def on_event_do(client, userdata, msg):
    print("Received message:", msg.topic, str(msg.payload.decode()))


def gateway_subscribe_to(topic):
    # Create and configure the MQTT client instance
    client = mqtt.Client()
    client.username_pw_set(username=username, password=password)

    # Assign callback function to handle incoming messages
    client.on_message = on_event_do

    # Connect to the MQTT broker and subscribe to specified topics
    client.connect(broker_address, port=port)

    client.subscribe(topic)

    # Start the network loop to process incoming messages (blocking call)
    client.loop_forever()



if __name__ == '__main__':

    # Define MQTT topic subscriptions
    #setTopics ( ["sensor/wh", "sensor/wv", "sensor/rp"])
    gateway_subscribe_to("sensor/wh")

import paho.mqtt.client as mqtt

# Define broker and connection settings
broker_address = "mqtt.example.com"
port = 1883
username = "your_username"
password = "your_password"

# Define MQTT topic subscriptions
topics = ["topic1", "topic2", "topic3"]

# Callback function when a message is received on subscribed topics
def on_message(client, userdata, msg):
    print("Received message:", msg.topic, str(msg.payload.decode()))

# Create and configure the MQTT client instance
client = mqtt.Client()
client.username_pw_set(username=username, password=password)

# Assign callback function to handle incoming messages
client.on_message = on_message

# Connect to the MQTT broker and subscribe to specified topics
client.connect(broker_address, port=port)
for topic in topics:
    client.subscribe(topic)

# Start the network loop to process incoming messages (blocking call)
client.loop_forever()

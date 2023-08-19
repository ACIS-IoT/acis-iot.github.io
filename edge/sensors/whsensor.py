import paho.mqtt.client as mqtt
import random

# MQTT broker details
broker_address = "mqtt.example.com"
broker_port = 1883
topic = "water/height"

# Create an MQTT client instance
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

def send_sensor_wh_data():
    # Simulate water height reading
    water_height = random.uniform(0.0, 10.0)  # Replace with actual measurement logic

    # Publish the water height reading to the specified topic on the MQTT broker
    client.publish(topic, str(water_height))

    print("Water Height:", water_height)

try:
    while True:
        send_sensor_wh_data()
        # Adjust sleep time based on how often you want to send data.
        time.sleep(5)  
        
except KeyboardInterrupt:
   print("Interrupted")
   client.disconnect()

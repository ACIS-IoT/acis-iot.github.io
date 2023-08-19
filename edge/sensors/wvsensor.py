import paho.mqtt.client as mqtt
import random

# MQTT broker details
broker_address = "mqtt.example.com"
broker_port = 1883

# MQTT topic to publish water volume readings
topic = "water/volume"

def simulate_water_sensor():
    # Simulate water level measurement between 0 and 100 (in percentage)
    water_level = random.randint(0, 100)

    # Create an MQTT client instance
    client = mqtt.Client()

    # Connect to the MQTT broker
    client.connect(broker_address, broker_port)

    # Publish the water volume reading to the specified topic
    client.publish(topic, str(water_level))

try:
    while True:
        simulate_water_sensor()
        # Adjust sleep time based on how often you want to send data.
        time.sleep(5)  
        
except KeyboardInterrupt:
   print("Interrupted")
   client.disconnect()

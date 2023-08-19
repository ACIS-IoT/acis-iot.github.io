import random
import time
import paho.mqtt.client as mqtt

# MQTT broker details
broker_address = "mqtt.example.com"
broker_port = 1883
topic = "rain/precipitation"

# Create MQTT client instance
client = mqtt.Client()

# Connect to the MQTT broker
client.connect(broker_address, broker_port)

def send_sensor_rp_data():
    # Generate random rainfall data between 0 and 100 mm/hr
    rainfall = round(random.uniform(0, 100), 2)
    
    # Publish the rainfall data to the MQTT topic
    client.publish(topic, str(rainfall))
    
    # Print the sent message for verification (optional)
    print(f"Rainfall: {rainfall} mm/hr")


try:
    while True:
        send_sensor_rp_data()
        # Adjust sleep time based on how often you want to send data.
        time.sleep(5)  
        
except KeyboardInterrupt:
   print("Interrupted")
   client.disconnect()

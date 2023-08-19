import paho.mqtt.client as mqtt
import random
import time

# MQTT broker details
broker_address = "broker.emqx.io"
username = "admin"
password = "admin"
broker_port = 1883

topicwh = "sensor/wh"
topicwv = "sensor/wv"
topicrp = "sensor/rp"

# Create an MQTT client instance
clientwh = mqtt.Client()

# Connect to the MQTT broker
clientwh.connect(broker_address, broker_port)

# Create an MQTT client instance
clientwv = mqtt.Client()

# Connect to the MQTT broker
clientwv.connect(broker_address, broker_port)

# Create an MQTT client instance
clientrp = mqtt.Client()

# Connect to the MQTT broker
clientrp.connect(broker_address, broker_port)


def send_sensor_data():
    while True:
        # Simulate water height reading
        water_height = random.uniform(0.0, 10.0)  # Replace with actual measurement logic

        # Publish the water height reading to the specified topic on the MQTT broker
        clientwh.publish(topicwh, str(water_height))

        print("Water Height:", water_height)

        # Generate random rainfall data between 0 and 100 mm/hr
        rainfall = round(random.uniform(0, 100), 2)

        # Publish the rainfall data to the MQTT topic
        clientrp.publish(topicrp, str(rainfall))

        # Print the sent message for verification (optional)
        print(f"Rainfall: {rainfall} mm/hr")

        # Simulate water level measurement between 0 and 100 (in percentage)
        water_level = random.randint(0, 100)

        # Publish the water volume reading to the specified topic
        clientwv.publish(topicwv, str(water_level))

        print("Water Volume:", water_level)

        # Adjust sleep time based on how often you want to send data.
        time.sleep(5)


def disconnect():
    clientrp.disconnect()
    clientwv.disconnect()
    clientwh.disconnect()

try:
    send_sensor_data()

except KeyboardInterrupt:
    print("Interrupted")
    disconnect()

import os
import random
import time
import json
from dotenv import load_dotenv
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

load_dotenv()

iot_endpoint = os.getenv("IOT_ENDPOINT")
certificate_path = os.getenv("CERTIFICATE_PATH")
private_path = os.getenv("PRIVATE_KEY_PATH")
root_ca_path = os.getenv("ROOT_CA_PATH")

client = AWSIoTMQTTClient("Device_parcial")
client.configureEndpoint(iot_endpoint, 8883)
client.configureCredentials(root_ca_path, private_path, certificate_path)

client.configureAutoReconnectBackoffTime(1, 32, 20)
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(30)

print("Conectando al cliente MQTT...")
client.connect()

def simulated_temperature():
  while True:

    temperature = round(random.uniform(20.0, 40.0), 2)
    light = round(random.uniform(0.0, 415.0), 2)
    humidity = round(random.uniform(45.0, 70.0), 2)
    nh3 = round(random.uniform(10.0, 30.0), 2)
    no2 = round(random.uniform(0.0, 0.6), 2)
    co = round(random.uniform(10.0, 50.0), 2)
    co2 = round(random.uniform(700.0, 1600.0), 2)

    message = {
      "device_id" : "temp_device",
      "timestamp" : int(time.time()),
      "temperature" : temperature,
      "humidity": humidity,
      "light": light,
      "NH3": nh3,
      "NO2": no2,
      "CO": co,
      "CO2": co2
    }

    print(f"Temperatura actual: {temperature} C")
    print(f"Humedad actual: {humidity} %")
    print(f"Luz actual: {light} lx")
    print(f"NH3 actual: {nh3} ppm")
    print(f"NO2 actual: {no2} ppm")
    print(f"CO actual: {co} ppm")
    print(f"CO2 actual: {co2} ppm")
    message_json = json.dumps(message)
    client.publish("iot/simulated/granja", message_json, 1)

    time.sleep(10)

try:
  simulated_temperature()
except KeyboardInterrupt:
  print("Simulación detenida.")
  client.disconnect()
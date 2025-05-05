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

    message = {
      "device_id" : "temp_device",
      "timestamp" : int(time.time()),
      "temperature" : temperature
    }

    print(f"Temperatura actual: {temperature} C")
    message_json = json.dumps(message)
    client.publish("iot/simulated/temperature", message_json, 1)

    time.sleep(2)

try:
  simulated_temperature()
except KeyboardInterrupt:
  print("Simulación detenida.")
  client.disconnect()
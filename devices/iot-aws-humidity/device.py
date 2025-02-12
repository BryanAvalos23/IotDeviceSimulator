import os
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from dotenv import load_dotenv
import random
import time
import json

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

HUMIDITY_THRESHOLD = 30.0

def simulate_soil_moisture():
  while True:
    soil_moisture = round(random.uniform(20.0, 40.0), 2)
    
    message = {
      "device_id": "humidity_device",
      "timestamp": int(time.time()),
      "humidity": soil_moisture,
      "irrigation": 0
    }
    
    if soil_moisture < HUMIDITY_THRESHOLD:
      message["irrigation"] = 1
      print(f"Humedad del suelo baja ({soil_moisture}%), activando riego.")
    else:
      print(f"Humedad del suelo adecuada ({soil_moisture}%). No se activa el riego.")
    
    message_json = json.dumps(message)
    client.publish("iot/simulated/irrigation", message_json, 1)
    
    time.sleep(10)

try:
  simulate_soil_moisture()
except KeyboardInterrupt:
  print("Simulación detenida.")
  client.disconnect()
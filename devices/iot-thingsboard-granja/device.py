import paho.mqtt.client as mqtt
import os
import random
import time
import json
from dotenv import load_dotenv

load_dotenv()

THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

def on_connect(client, userdata, flags, rc):
  if rc == 0:
    print("Conectado exitosamente a ThingsBoard!")
  else:
    print(f"Error de conexión: {rc}")

client = mqtt.Client()
client.username_pw_set(ACCESS_TOKEN)
client.on_connect = on_connect

client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()

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
        "device_id": "temp_device",
        "timestamp": int(time.time()),
        "temperature": temperature,
        "humidity": humidity,
        "light": light,
        "NH3": nh3,
        "NO2": no2,
        "CO": co,
        "CO2": co2
      }

      print("Datos enviados")
      message_json = json.dumps(message)
      
      client.publish("v1/devices/me/telemetry", message_json, 1)

      time.sleep(15)

try:
    simulated_temperature()
except KeyboardInterrupt:
    print("Simulación detenida.")
    client.loop_stop()
    client.disconnect()

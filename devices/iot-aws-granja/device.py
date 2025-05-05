import os
import random
import time
import json
from dotenv import load_dotenv
from colorama import Fore, Style
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

print(Fore.BLUE + "\n[+] Conectando al cliente MQTT...\n" + Style.RESET_ALL)
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

    print(Fore.GREEN + "[+] Nuevo mensaje publicado:" + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + "=========================================" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [+]" + Style.RESET_ALL + " Temperatura actual: " + Fore.GREEN + str(temperature) + " C" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [+]" + Style.RESET_ALL + " Humedad actual: " + Fore.GREEN + str(humidity) + " %" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [+]" + Style.RESET_ALL + " Luz actual: " + Fore.GREEN + str(light) + " LUX" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [+]" + Style.RESET_ALL + " NH3 actual: " + Fore.GREEN + str(nh3) + " ppm" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [+]" + Style.RESET_ALL + " NO2 actual: " + Fore.GREEN + str(no2) + " ppm" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [+]" + Style.RESET_ALL + " CO actual: " + Fore.GREEN + str(co) + " ppm" + Style.RESET_ALL)
    print(Fore.YELLOW + "   [+]" + Style.RESET_ALL + " CO2 actual: " + Fore.GREEN + str(co2) + " ppm" + Style.RESET_ALL)
    print(Fore.LIGHTYELLOW_EX + f"=========================================\n" + Style.RESET_ALL)
    
    message_json = json.dumps(message)
    client.publish("iot/simulated/granja", message_json, 1)

    time.sleep(10)

try:
  simulated_temperature()
except KeyboardInterrupt:
  print("Simulación detenida.")
  client.disconnect()
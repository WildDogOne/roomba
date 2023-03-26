import json
import ssl
import time
from paho.mqtt import client as mqtt_client

from content.creds import ROOMBA_IP, ROOMBA_PASSWORD, ROOMBA_BLID

ROBOT_IP = ROOMBA_IP
ROBOT_BLID = ROOMBA_BLID
ROBOT_PASSWORD = ROOMBA_PASSWORD


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to Roomba MQTT server")
        client.subscribe("mission")
    else:
        print("Failed to connect")


def on_message(client, userdata, msg):
    message = json.loads(msg.payload)

    if "maps" in message:
        maps = message["maps"]
        for m in maps:
            if "regions" in m:
                print("Room Information:")
                for region in m["regions"]:
                    print(f"{region['name']}: {region['id']}")

        client.disconnect()


client = mqtt_client.Client(client_id=ROBOT_BLID, transport="tcp")
client.username_pw_set(ROBOT_BLID, ROBOT_PASSWORD)
client.tls_set(cert_reqs=ssl.CERT_NONE)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message

client.connect(ROBOT_IP, 8883)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
client.loop_start()

# Wait for the connection to close
while client.is_connected():
    time.sleep(1)

client.loop_stop()

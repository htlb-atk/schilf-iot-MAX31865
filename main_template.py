import time
import machine
from network import WLAN
from umqtt.robust import MQTTClient

from lopy_max31865 import MAX31865

# connect to WLAN
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    # if net.ssid == 'WLAN-HTLB':
    if net.ssid == 'WLAN-HTLB':
        print('Network found!')
        wlan.connect(net.ssid, auth=(WLAN.WPA2, 'xxxxxxxxxx'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

# create MAX31865 object
rtd = MAX31865()

# Connect to thingspeak; password= MQTT API Key
thingspeak = MQTTClient("fe058e3f82b94a968fb8bc105b36dc", "52.5.134.229", port=1883, user="atkhtlb", password="MQTT_API_KEY")
thingspeak.DEBUG = True
thingspeak.connect(clean_session=True)
while True:
    temp = rtd.read()
    print('Temperatur: ',temp)
    # publish temp
    thingspeak.publish("channels/347424/publish/fields/field1/WRITE_API_KEY",str(temp));

    time.sleep(30)
thingspeak.disconnect()

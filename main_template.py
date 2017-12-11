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
    if net.ssid == 'Silkur':
        print('Network found!')
        # wlan.connect(net.ssid, auth=(WLAN.WPA2, ''), timeout=5000)
        wlan.connect(net.ssid, auth=(WLAN.WPA2, '***REMOVED***'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

time.sleep(2)
# create MAX31865 object
rtd = MAX31865()

thingspeak = MQTTClient(client_id="fe058e3f82b94a968fb8bc105b36dc", server="52.5.134.229", port=1883, user="atkhtlb", password="***REMOVED***")
thingspeak.DEBUG = True
thingspeak.connect(clean_session=True)
while True:
    temp = rtd.read()
    print('Temperatur: ',temp)
    # publish temp
    thingspeak.publish("channels/347424/publish/fields/field1/***REMOVED***",str(temp));

    time.sleep(30)
thingspeak.disconnect()

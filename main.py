import time
import machine
from network import WLAN
from umqtt.robust import MQTTClient

from MAX31865 import MAX31865

# connect to WLAN
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == 'WLAN-HTLB':
    # if net.ssid == 'Silkur':
        print('Network found!')
        # wlan.connect(net.ssid, auth=(WLAN.WPA2, ''), timeout=5000)
        wlan.connect(net.ssid, auth=(WLAN.WPA2, '0000000000'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break

time.sleep(2)
rtd = MAX31865()


adc = machine.ADC()             # create an ADC object
apin = adc.channel(pin='P13', attn=ADC_ATTN_0DB)   # create an analog pin on P13
val = apin()                    # read an analog value


thingspeak = MQTTClient("device_id", "34.192.179.155", port=1883)
thingspeak.DEBUG = True
thingspeak.connect()
while True:
    temp = rtd.read()
    print('Temperatur: ',temp)
    val=apin()
    print('Strom: ', val)
    # publish temp
    thingspeak.publish("channels/347424/publish/fields/field1/***REMOVED***",str(temp));

    time.sleep(30)
thingspeak.disconnect()

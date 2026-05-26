
# MBB (My Buddy Buoy :D) reciever


import network
import time
from machine import Pin

#credentials
ssid = "my-wifi"
password = "password"


led = Pin("LED", Pin.OUT) #led pin

# make board led blink infinite for error
def blink(): 
    
    while True:
        led.value(1)
        time.sleep(0.5) 
        led.value(0)
        time.sleep(0.5)

#connect to wifi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    network.hostname("MTB Reciever")

    time_start = time.ticks_ms() # IF wifi buffers for more than X seconds, restart wifi.
    while not wlan.isconnected:
        if time.ticks_diff(time.ticks_ms(), time_start) > 30 * 1000: #if >30 secs
            break
        time.sleep_ms
    return wlan

#Connections
try:
    connect()
    for i in range (3):
        led.value(1)
        time.sleep(0.25) 
        led.value(0)
        time.sleep(0.25)

except OSError as e: #if really bad error, blink forever
    blink()
    print("Wifi Error")

#Sleep before program to give USBs more time to setup
try: 
    time.sleep_ms(200)

except Exception:
    pass


    
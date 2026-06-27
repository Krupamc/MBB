
# MBB (My Buoy Buddy :D) receiver


import network
import time
from machine import Pin
import config as cfg
import ntptime

#credentials
ssid = cfg.ssid
password = cfg.password

led = Pin("LED", Pin.OUT) #led pin

# make board led blink infinite for error
def blink(): 
    
    while True:
        led.value(1)
        time.sleep(0.5) 
        led.value(0)
        time.sleep(0.5)

# Connect to wifi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    network.hostname(cfg.hostname)

    time_start = time.ticks_ms() # IF wifi buffers for more than X seconds, restart wifi.
    while not wlan.isconnected():
        if time.ticks_diff(time.ticks_ms(), time_start) > cfg.buffer_time * 1000:
            break
        time.sleep_ms(100)
    return wlan

# Sync Time with NTP Server
days_of_week = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Offset based on Timezone
utc = cfg.utc_offset

def sync_wifi_time():
    try:
        ntptime.settime()
        print("Time Synced with NTP")

    except Exception as e:
        print("Error syncing time:", e)

def formatted_time():
    now = time.localtime(time.time() + cfg.utc_offset * 3600)

    formatted_datetime = (
        f"{days_of_week[now[6]]}, "
        f"{now[0]:04d}-{now[1]:02d}-{now[2]:02d} "
        f"{now[3]:02d}:{now[4]:02d}:{now[5]:02d}"
    )
    return formatted_datetime

# Connections
try:
    connect()
    for i in range (3):
        led.value(1)
        time.sleep(0.25) 
        led.value(0)
        time.sleep(0.25)
        led.value(1)
        time.sleep(2)
        led.value(0)
    print("WIFI Connected")
        
except OSError as e: # If really bad error, blink forever
    blink()
    print("Wifi Error")

try:
    sync_wifi_time()
    for i in range (3):
        led.value(1)
        time.sleep(0.25) 
        led.value(0)
        time.sleep(0.25)
        led.value(1)
        time.sleep(2)
        led.value(0)
    print("Time Synced")

except OSError as e: # If really bad error, blink forever
    blink()
    print("Time Error")
    
# Sleep before program to give USBs more time to setup
try: 
    time.sleep_ms(200)

except Exception:
    pass


    
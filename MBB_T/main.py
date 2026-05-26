# Starting Script

import machine, time
import wtemp # DS18B20 Water Probe
import GPS # NEO-6M GPS
import rtc #DS3231 RTC
import config as cfg

def read():

    # Water Temperature
    temp_c = wtemp.watertmp()

    if temp_c is None:
        print("No DS18B20 found")
    else:
        print("Water temp (C): {:.2f}".format(temp_c))

    # GPS
    gps_d = GPS.get_gps()

    # Battery Voltage

def timestamp():
    #timestamp the data together
    data = "easy"

def save():
    # Save to a microsd card
    sd ="cool"

def transmit():
    # Transmit to LoRa and write down missing packets to send later...
    lora = "stupid"

def main():
    rtc.sync_if_lost_power()
    rtc.clear_alarm()
    rtc.setup_alarm(cfg.alarm_interval) # CAHNGE TO 60 LATER in config
    while True:
        read()
       
        time.sleep(10) # remove for deepsleep later
    #machine.deepsleep

if __name__ == "__main__":
    main()
# Starting Script

import machine, time
import wtemp # DS18B20 Water Probe
import GPS # NEO-6M GPS
import rtc # DS3231 RTC
import log # Microsd Card logging
import lora_tx as lora # LoRa Tranmission
import config as cfg

def read_water_temp():
    # Water Temperature
    try:
        temp_c = wtemp.watertmp()
    
    except Exception as e: # Errors will be sent with the rest of the data as a string; an error message starts with "*"
        temp_c = "*" + str(e)
        print(e)

    if isinstance(temp_c, str):
        print("No DS18B20 found")
    else:
        print("Water temp (C): {:.2f}".format(temp_c))
    
    return temp_c

def read_gps():
    # GPS
    gps_d = GPS.get_gps() # Sends a error back as a string if there is one
    return gps_d

def read_time():
    # RTC - Real Time Clock
    time_rtc = rtc.formatted_time()
    return time_rtc

def read_battery():
    # Battery Voltage
    bat_v = "insert function"
    return bat_v

def build_record():
    # Combine the data together
    temp_c = read_water_temp()
    timestamp = read_time()
    in_temp = rtc.get_temp_c
    gps_lat = GPS.get_lat()
    gps_lon = GPS.get_long()
    gps_alt = GPS.get_alt()
    gps_sats = GPS.get_sats()
    gps_hdop = GPS.get_hdop()
    gps_d = read_gps()

    record = { # Directory of all data values to be saved and trasmitted
        "timestamp": timestamp,
        "water_temp_c": temp_c,
        "gps_lat": gps_lat,
        "gps_lon": gps_lon,
        "gps_alt": gps_alt,
        "gps_sats": gps_sats,
        "gps_hdop": gps_hdop,
        "internal_temp": in_temp,
        "batt_v": None,      # replace later
        "seq": None,            # replace later
    }

    return record
    
    

def save_record(record):
    # Save to a microsd card
    log.save_sample(record)

def transmit_record(record):
    # Transmit to LoRa and write down missing packets to send later...
    lora.transmit(record)

def run_cycle():
    record = build_record()
    save_record(record)
    time.sleep_ms(500)
    transmit_record(record)

def main():
    rtc.sync_if_lost_power()
    rtc.clear_alarm()
    rtc.setup_alarm(cfg.alarm_interval) # CAHNGE TO 60 LATER in config
    while True:
        record = run_cycle()
       
        time.sleep(10) # remove for deepsleep later
    record = run_cycle()
    
    #machine.deepsleep

if __name__ == "__main__":
    main()
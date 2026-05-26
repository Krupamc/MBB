# Configuration of the MBB (My Buddy Buoy :D) Reciever:

#LoRa

lora_frq_khz = 915000  # 915 MHz for North America; use 868000 for EU

lora_cfg = {
    "freq_khz": lora_frq_khz,
    "sf": 7,                 # spreading factor
    "bw": "125",             # 125 kHz bandwidth
    "coding_rate": 5,        # 4/5
    "preamble_len": 8,
    "output_power": 14,      # dBm (respect local limits)
    "implicit_header": False,
    "crc_en": True,
    "syncword": 0x12,
    "dio3_tcxo_millivolts": 1800,
    "use_regulator_ldo": True,
}

lora_gpio = [2,3,10,11,12,15,20,26] #issue due to how RTC also wants gpio 20: see plan doc
spi_id = 1
pin_sck = 10
pin_mosi = 11
pin_miso = 12
pin_cs = 3
pin_dio1 = 20
pin_rst = 15
pin_busy = 2
bad_ad = 26
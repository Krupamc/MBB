#Buoy transmitter with micropySX126X lib
#https://github.com/ehong-tl/micropySX126X

from machine import Pin, SPI
from time import sleep
from lora import SX1262 #change lib folder to lora btw
import config as cfg
import log

def init_lora():
    spi = SPI(
        cfg.spi_id,
        baudrate=2_000_000,
        polarity=0,
        phase=0,
        bits=0,
        firstbit=SPI.MSB,
        sck=Pin(cfg.pin_sck),
        mosi=Pin(cfg.pin_mosi),
        miso=Pin(cfg.pin_miso),
        )
    
    lora = SX1262(
        spi=SPI,
        cs=Pin(cfg.pin_cs, Pin.OUT),
        irq=Pin(cfg.pin_dio1, Pin.IN),
        rst=Pin(cfg.pin_rst, Pin.OUT),
        busy=Pin(cfg.pin_busy, Pin.IN) if cfg.pin_busy is not None else None,
        lora_cfg=cfg.lora_cfg,
    )
    return lora

def transmit_test(msg):
    lora = init_lora()
    print("LoRa TX ready (freq {} kHz)".format(cfg.lora_cfg["freq_khz"]))

    counter = 0
    while True:
        #change to just be 1 time
        msg = "buoy ping {}".format(counter) #also send the number of bits/items
        print("TX:", msg)
        lora.send(msg.encode("utf-8"))
        counter += 1
        sleep(5)

def transmit(msg, seq):
    #lora = init_lora()
    print("LoRa TX ready (freq {} kHz)".format(cfg.lora_cfg["freq_khz"]))
    
    #change to be just once
    msg.format(seq) #also send the number of bits/items
    print("TX:", msg)
    lora.send(msg.encode("utf-8"))

def resend_sequence(seq_needed):
    print("LoRa TX ready for Resend (freq {} kHz)".format(cfg.lora_cfg["freq_khz"]))

    msg = log.read_sample(seq_needed) # Read the data from the monthly csv
    
    msg = "buoy ping {}".format(seq_needed) #also send the number of bits/items
    print("TX:", msg)
    lora.send(msg.encode("utf-8"))

#if __name__ == "__main__":
#    main()

# WORKING ON T
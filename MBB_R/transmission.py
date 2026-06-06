from machine import Pin, SPI
from time import sleep
from lora import SX1262 #change lib folder to lora btw
import config as cfg # Config
import log # Saving to MicroSD

def make_missing_record(record, seq, last_seq):
    missing_record = {
        "rx_timestamp": "replace", # Change this with wifi time speicifed earlier
        "expected_from": last_seq + 1,
        "expected_to": seq - 1,
        "received_seq": seq,
    }
    log.save_missing(missing_record)

def ask_missing():
    #MAKE THIS
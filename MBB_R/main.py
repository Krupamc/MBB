import machine, time
import sd_storage as sd # Mounting the Microsd card
import log # Microsd Card logging
import lora_rx as lora # LoRa Tranmission
import config as cfg

def main():
    print(f"Board Powered on!\n")
    
    # Mount and turn on LoRa/Microsd Card
    mount = sd.mount_sd()
    lora_device = lora.init_lora()
    
    seq = log.what_is_next_sequence()
    print(f"Welcome to the {seq} sampling of the {cfg.buoy_name}!\nAll data will be collected, saved, and transmitted to the Reciever on the shore.\n")
    
    # Wait for packets
    while True:
        record = lora.recieve_once()

        if record is not None:
            print("RX Record:", record)
            log.save_sample(record)
            log.missing_check()
        
        time.sleep(0.1)



if __name__ == "__main__":
    main()
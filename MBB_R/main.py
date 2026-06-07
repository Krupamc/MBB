import machine, time
import sd_storage as sd # Mounting the Microsd card
import log # Microsd Card logging
import lora_rx as lora # LoRa Receiving
import lora_tx as tx # LoRa Transmitting
import config as cfg
import boot # Time Syncing and WIFI

# Retry a function
def retry_operation(func, record, attempts=3, delay_ms=500, name="operation"):
    for attempt in range(1, attempts + 1):
        ok = func(record)
        if ok:
            return True

        print(f"[ERROR] {name} attempt {attempt}/{attempts} failed")
        if attempt < attempts:
            time.sleep_ms(delay_ms)

    return False

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
            seq_status = log.check_sequence(record)
            missing = seq_status.get("missing_seqs")
            if missing:
                tx.ask_missing(seq_status["missing_seqs"])

            log.save_sample(record)
        time.sleep(0.1)



if __name__ == "__main__":
    main()
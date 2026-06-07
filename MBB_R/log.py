import os

import sd_storage
import lora_tx as tx

log_dir = "/sd/logs"
seq_dir = "/sd/seq.txt"
time_dir = "/sd/time.txt"

header = [ # All csv headers
    "rx_timestamp,"
    "timestamp,"
    "water_temp_c,"
    "gps_lat,"
    "gps_lon,"
    "gps_alt,"
    "gps_sats,"
    "gps_hdop,"
    "internal_temp,"
    "batt_v,"
    "seq,"
    "temp_error,"
    "gps_error,"
    "rtc_error,"
    "internal_temp_error,"
    "batt_error,"
    "rssi,"
    "snr,"
    "raw_payload,"
    ]

# Set SAMPLE Time
def set_sample_time(formatted_time):

    try:
        with open(time_dir, "r") as f:
            global sample_time
            sample_time = f.read().strip()
            return sample_time
    except:
        return 0

def read_sample_time():
    try:
        with open(time_dir, "r") as f:
            return int(f.read().strip())
    except:
        return 0 

# Monthly csvs 
def get_monthly_filename(): 
    dt = sample_time
    year = dt[0]
    month = dt[1]
    fname = "{:04d}-{:02d}.csv".format(year, month)
    return log_dir + "/" + fname

def ensure_header(path):
    # If file doesn't exist or is empty, write a header row
    try:
        size = os.stat(path)[6]
    except OSError:
        size = 0

    if size == 0:
        with open(path, "w") as f:
            f.write(header)
            f.close

# Append the record to the monthly csv
def save_sample(record):
    
    path = get_monthly_filename()
    ensure_header(path)

    # Build CSV line
    row = []
    for key in header:
        value = record.get(key, "")
        row.append(str(value))

    line = ",".join(row) + "\n"

    with open(path, "a") as f:
        f.write(line)
        f.flush()
        
    f.close()

# Append the missing record to a csv
def save_missing(missing_record):

    path = "/sd/logs/missing_records.csv"
    ensure_header(path)

    # Build CSV line
    row = []
    for key in header:
        value = missing_record.get(key, "")
        row.append(str(value))

    line = ",".join(row) + "\n"

    with open(path, "a") as f:
        f.write(line)
        f.flush()
        
    f.close()

# Following functions are for R/W the Sequence #
def load_seq():
    try:
        with open(seq_dir, "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_seq(seq):
    with open(seq_dir, "w") as f:
        f.write(str(seq))

def next_sequence():
    seq = load_seq() + 1
    save_seq(seq)
    return seq

def what_is_next_sequence():
    seq = load_seq() + 1
    return seq

# Check if the sequence value
def check_sequence(record):

    seq = int(record["seq"]) # Get Seq
    last_seq = load_seq()

    result = { # Directory of status
        "first_time": False,
        "duplicate": False,
        "out_of_order": False,
        "ok": False,
        "old": False,
        "missing_seqs": []
    }

    if seq == last_seq + 1: #No Errors
        print(f"[SEQ]: Sequence is {seq}")
        result["ok"] = True
        next_sequence()
    
    elif seq == last_seq: # First time
        print("[FIRST BOOT]: Welcome to the First Sequence!!!")
        result["first_time"] = True
        next_sequence()
    
    elif seq == last_seq: # Duplicate
        print("[SEQ Warning]: Received the Same Packet; Ignored")
        result["duplicate"] = True
    
    elif seq < last_seq: # Old Packet
        print("[SEQ Warning]: Received an Old Packet; Ignored")
        result["old"] = True
        
    
    elif seq == last_seq + 2: # Missing the Last packet
        print("[SEQ ERROR]: Missing Packet(s); Asking for Last Packet")
        result["missing_seqs"] = list(range(last_seq + 1, seq))
    
    else: # Will sort at server
        print("[SEQ Warning]: Out of Order; Saving regardless")

    missing = result.get("missing_seqs")
    
    if missing:
        print(f"Found {len(missing)} missing packets")
        tx.make_missing_record(record, seq, last_seq)

    
    return result
    
    
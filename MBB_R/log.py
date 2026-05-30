import os
import rtc   # your RTC helper, returning dt.year, dt.month...
import sd_storage

log_dir = "/sd/logs"
seq_dir = "/sd/seq.txt"

header = [ # All csv headers
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
     "batt_error"
    ]

# Monthly csvs 
def get_monthly_filename(): 
    dt = rtc.get_datetime()
    fname = "{:04d}-{:02d}.csv".format(dt.year, dt.month)
    return log_dir + "/" + fname

def ensure_monthly_header(path):
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
    """
    sample: dict with keys matching CSV header.
    """
    path = get_monthly_filename()
    ensure_monthly_header(path)

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
        
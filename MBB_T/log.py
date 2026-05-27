import os
import rtc   # your RTC helper, returning dt.year, dt.month...
import sd_storage

LOG_DIR = "/sd/logs"

header = [ # All csv headers
    "timestamp,"
    "water_temp_c,"
    "lat,"
    "lon,"
    "altitude,"
    "satellites,"
    "hdop,"
    "batt_v,"
    "internal_temp"
    "seq"
    ]

# Monthly csvs 
def get_monthly_filename(): 
    dt = rtc.get_datetime()
    fname = "{:04d}-{:02d}.csv".format(dt.year, dt.month)
    return LOG_DIR + "/" + fname

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
        
    f.close
        
import os
import rtc   # your RTC helper, returning dt.year, dt.month...
import sd_storage

LOG_DIR = "/sd/logs"

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
            f.write("timestamp,water_temp_c,lat,lon,batt_v,seq\n")

def append_sample(sample):
    """
    sample: dict with keys matching CSV header.
    """
    path = get_monthly_filename()
    ensure_monthly_header(path)

    # Build CSV line
    line = "{ts},{wt:.2f},{mx:.3f},{my:.3f},{mz:.3f},{lat:.6f},{lon:.6f},{bv:.3f},{seq}\n".format(
        ts=sample["timestamp"],
        wt=sample["water_temp_c"],
        mx=sample["mag_x"],
        my=sample["mag_y"],
        mz=sample["mag_z"],
        lat=sample["lat"],
        lon=sample["lon"],
        bv=sample["batt_v"],
        seq=sample["seq"],
    )

    with open(path, "a") as f:
        f.write(line)
        f.flush()
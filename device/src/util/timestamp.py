import ntptime
import time

def sync_time():
    is_synced = False
    while not is_synced:
        try:
            ntptime.settime()
            print("time synced with ntp")
            is_synced = True
        except:
            time.sleep(1)

def get_jst_struct_time():
    return time.localtime(time.time() + 9 * 3600)

def get_jst_date():
    t = get_jst_struct_time()
    return '{:04d}-{:02d}-{:02d}'.format(t[0], t[1], t[2])

def get_jst_time():
    t = get_jst_struct_time()
    return '{:02d}:{:02d}:{:02d}'.format(t[3], t[4], t[5])

def get_jst_datetime():
    return '{} {}'.format(get_jst_date(), get_jst_time())

import datetime

def get_timestamp_str():
    return str(int(datetime.datetime.timestamp(datetime.datetime.now())))
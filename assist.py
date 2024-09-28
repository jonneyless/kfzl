import time


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def get_current_timestamp():
    return int(time.time())


def time2timestamp(t, flag=True):
    if flag:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d %H:%M:%S')))
    else:
        return int(time.mktime(time.strptime(t, '%Y-%m-%d')))


def timestamp2time(t):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

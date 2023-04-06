import time

def localtime():
    # seconds passed since January 1st, 1970 at midnight
    seconds = time.time()

    # convert the epoch time in seconds to a readable format
    local_time = time.ctime(seconds)
    print("Local time:", local_time)
    return local_time


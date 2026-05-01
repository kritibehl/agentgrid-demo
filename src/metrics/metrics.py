import time

def measure(fn, *args):
    start = time.time()
    result = fn(*args)
    latency = time.time() - start
    return result, latency

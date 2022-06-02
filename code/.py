import time
y=time.perf_counter()
delay=10
while 1:
    if y+delay<time.perf_counter():
        print('yes')
        y=time.perf_counter()
    else:print('no')
    time.sleep(1)
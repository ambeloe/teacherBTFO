import time
import datetime

while True:
    now = datetime.time.now()
    if now.hour == 0 and now.minute == 0:
        exec("main.py")
    time.sleep(50)

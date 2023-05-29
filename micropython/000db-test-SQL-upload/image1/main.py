import machine
from time import sleep

# import logger
import sd
import thermocouple
import lcd

print("START")

print("good to go")

# LogMount = "/logs/"
# TestLog =" /logs/testlog.log"

# logger.get_storage_stats('/logs')

# t1, t1c, t2 = thermocouple.takereading()

sleep(0.1)
fn = "/logs/one-line-log.txt"

for i in range(20):
    t1, t1c, t2 = thermocouple.takereading()

    with open(fn, "a") as f:
        n = f.write(f"{i}\t{time.localtime()}\t{t1}\t{t1c}\t{t2}")
        print(f"{time.localtime()}\tt1: {t1:6}\t t1c: {t1c:6}\tt2: {t2:6}")
        # f.write(f"{t1}")
        print(n, "bytes written")
        f.write("\n")

    sleep(1)

print("dump contents")
fn = "/logs/one-line-log.txt"
with open(fn, "r") as f:
    for line in f:
        print(line.rstrip())
print("end of log")

# ########### !!! if you don't close it, it will get overwritten
# when the next PYMAKR update is performed!!!!!!!!!!!
# sd.closeSD()

# logger.write_log("This is a test.", TestLog)
# while True:

#     sleep(1)

import machine
from time import sleep

# import logger
import realtc
import sd
import thermocouple
import lcd

print("START")

print("good to go")


# sleep(0.1)
log = conf.LOG_MOUNT + "/" + conf.LOG_FILENAME

for i in range(20):
    t1, t1c, t2 = thermocouple.takereading()

    with open(log, "a") as f:
        f.write(f"{i}\t{realtc.formattime(time.localtime())}\t{t1}\t{t1c}\t{t2}\n")
        # f.write("\n")
        print(f"{realtc.formattime(time.localtime())}\tt1: {t1:6}\t t1c: {t1c:6}\tt2: {t2:6}")

    sleep(1)

print("dump contents")
with open(log, "r") as f:
    for line in f:
        print(line.rstrip())
print("end of log")

# ########### !!! if you don't close it, it will get overwritten
# when the next PYMAKR update is performed!!!!!!!!!!!
sd.closeSD(conf.LOG_MOUNT)


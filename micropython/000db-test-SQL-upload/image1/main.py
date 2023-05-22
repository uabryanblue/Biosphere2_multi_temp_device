import machine
from time import sleep
# import logger
import sd
import thermocouple

print("START")

print("good to go")

# LogMount = "/logs/"
# TestLog =" /logs/testlog.log"

# logger.get_storage_stats('/logs')

t1 = thermocouple.takereading()
sleep(0.1)
fn = "/logs/one-line-log.txt"
with open(fn, "a") as f:
    n = f.write("duhuh: ")
    f.write(f"{t1}")
    print(n, "bytes written")
    f.write('\n')

print("dump contents")
fn = "/logs/one-line-log.txt"
with open(fn, "r") as f:
    for line in f:
        print(line)
print("end of log")

# sd.closeSD()

# logger.write_log("This is a test.", TestLog)
# while True:

#     sleep(1)
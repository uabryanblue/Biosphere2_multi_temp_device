import machine
from time import sleep
import logger

print("START")

print("good to go")

# LogMount = "/logs/"
# TestLog =" /logs/testlog.log"

logger.get_storage_stats('/logs')

fn = "/logs/one-line-log.txt"
with open(fn, "a") as f:
    n = f.write("blah\nblah2\n")
    print(n, "bytes writtein")

# logger.write_log("This is a test.", TestLog)
# while True:

#     sleep(1)
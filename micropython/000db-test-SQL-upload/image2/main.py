import machine
from time import sleep

# import logger
import conf
import realtc
import sd
import thermocouple
import espnowex

print("START")

print("good to go")


# sleep(0.1)
# log = conf.LOG_MOUNT + "/" + conf.LOG_FILENAME




con = espnowex.init_rx()

for i in range(100):

    # TODO this needs to be read from configuration
    readings = dict()
    readings[1] = 0.0
    readings[2] = 0.0
    readings[3] = 0.0
    readings[4] = 0.0
    readings[5] = 0.0

    readings = thermocouple.read_thermocouples(readings)

  
    for key in readings.keys():
        print(f"key: {key}, value: {readings[key]}")
    out = ','.join(map(str, readings.values()))
    print(out)
    espnowex.demo_send(con, out)
    # with open(log, "a") as f:
    #     f.write(f"{i}\t{realtc.formattime(time.localtime())}")
    #     for key in readings.keys():
    #         print(f"key: {key}, value: {readings[key]}")
    #         f.write(f"\t{readings[key]}")
    #     f.write("\n")

    sleep(1)

# print("dump contents")
# with open(log, "r") as f:
#     for line in f:
#         print(line.rstrip())
# print("end of log")




# ########### !!! if you don't close it, it will get overwritten
# when the next PYMAKR update is performed!!!!!!!!!!!
# sd.closeSD(conf.LOG_MOUNT)


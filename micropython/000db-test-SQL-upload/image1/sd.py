# CUSTOM CODE TO MOUNT MICROSD CARD
# DATA SHOULD GO TO /mnt/log/



import machine, sdcard, os

# MicroSD card adaptor is interfaced via SPI 1
sd = sdcard.SDCard(machine.SPI(1), machine.Pin(27))

# mount /fc as the sd card
vfs = os.VfsFat(sd)
os.mount(vfs, “/fc”)
print(“Filesystem check”)
print(os.listdir(“/fc”))


# writing a single block in a text file on a MicroSD card
fn = “/fc/one-line-log.txt”
print()
print(“Single block write”)
with open(fn, “w”) as f:
            n = f.write('1234567890\n')  # one block
            print(n, “bytes written”)


# reading a text file from a MicroSD card
fn = “/fc/one-line-log.txt”
print()
print(“Single block read”)
with open(fn, “r”) as f:
            result = f.read()
            print(len(result2), “bytes read”)
            print()
            print(result)


#writing multiple blocks in a text file on a MicroSD card
line = 'abcdefghijklmnopqrstuvwxyz\n'
lines = line * 200  # 5400 chars
fn = “/fc/multi-line-log.txt”
print()
print(“Multiple block write”)
with open(fn, “w”) as f:
            n = f.write(lines)
            print(n, “bytes written”)

# reading multi-block text file from a MicroSD card.

fn = “/fc/multi-line-log.txt”
print()
print(“Multiple block read”)
with open(fn, “r”) as f:
            result = f.read()
            print(len(result2), “bytes read”)
            print()
            print(result)            
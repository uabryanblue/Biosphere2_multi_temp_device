

import espnow
import network
import time

def get_mac():
    """ get the MAC address and return it as a binary value
    use this to get human readable
    ':'.join(['{:02x}'.format(b) for b in espnowex.get_mac()])
    """
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    wlan_mac = wlan_sta.config('mac')
    
    return wlan_mac


def demo_send(e, msg):
    print("run demo_send")
    # sta = network.WLAN(network.STA_IF)    # Enable station mode for ESP
    # sta.active(True)
    # sta.disconnect()        # Disconnect from last connected WiFi SSID

    # e = espnow.ESPNow()     # Enable ESP-NOW
    # e.active(True)

    # # MAC address of peer1's wifi interface exmaple:
    # # peer1 = b'\xe8\x68\xe7\x4e\xbb\x19'
    peer1 = b'\x8c\xaa\xb5M\x7f\x18'  # my #2 esp8266
    # e.add_peer(peer1)                     # add peer1 (receiver1)

    # peer2 = b'\x60\x01\x94\x5a\x9c\xf0'   # MAC address of peer2's wifi interface
    # e.add_peer(peer2)                     # add peer2 (receiver2)

    print("Starting...")            # Send to all peers

    e.send(peer1, msg, True)     # send commands to pear 1
    # # e.send(peer2, "walk", True)     # send commands to pear 2
    # time.sleep_ms(2000)
    # e.send(peer1, "back", True)
    # # e.send(peer2, "back", True)
    # time.sleep_ms(2000)
    # e.send(peer1, "stop", True)
    # # e.send(peer2, "back", True)
    # e.send(peer1, "fail", True)
    # # e.send(peer2, "back", True)

    print("done demo_send")

def init_rx():
    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect()                # Disconnect from last connected WiFi SSID

    e = espnow.ESPNow()                  # Enable ESP-NOW
    e.active(True)

    # MAC address of peer's wifi interface
    # example: b'\x5c\xcf\x7f\xf0\x06\xda'
    peer = b'\x8c\xaa\xb5M\x7f\x18' # my esp8266 #1
    e.add_peer(peer)                   # Sender's MAC registration

    return e

def demo_rx():

    # A WLAN interface must be active to send()/recv()
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.disconnect()                # Disconnect from last connected WiFi SSID

    e = espnow.ESPNow()                  # Enable ESP-NOW
    e.active(True)

    # MAC address of peer's wifi interface
    # example: b'\x5c\xcf\x7f\xf0\x06\xda'
    peer = b'\xec\xfa\xbc\xcb\xab\xce' # my esp8266 #1
    e.add_peer(peer)                   # Sender's MAC registration

    while True:
        host, msg = e.recv()
        if msg:                          # wait for message
            if msg == b'walk':           # decode message and translate
                print("kwkF")       
            elif msg == b'back':
                print('kbk')
            elif msg == b'stop':
                print('d')

if __name__ == "__main__":
    espnow_rx()
    
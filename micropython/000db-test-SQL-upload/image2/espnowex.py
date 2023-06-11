

import espnow
import network
import time

import network, time

def wifi_reset():   # Reset wifi to AP_IF off, STA_IF on and disconnected
    sta = network.WLAN(network.STA_IF); sta.active(False)
    ap = network.WLAN(network.AP_IF); ap.active(False)
    sta.active(True)
    while not sta.active():
        time.sleep(0.1)
    sta.disconnect()   # For ESP8266
    while sta.isconnected():
        time.sleep(0.1)
    return sta, ap

def init_esp_connection(sta):
    """creates and espnow object, wifi_reset() needs called before this"""
    # create espnow connection
    e = espnow.ESPNow()
    e.active(True)

    # MAC address of peer's wifi interface
    # example: b'\x5c\xcf\x7f\xf0\x06\xda'
    # TODO peers should be in the conf file
    peer = b'\x8c\xaa\xb5M\x7f\x18' # my esp8266 #1
    e.add_peer(peer) # register the peer for espnow communication

    return e


def get_mac(wlan_sta):
    """ get the MAC address and return it as a binary value
    change binary to human readable:
    ':'.join(['{:02x}'.format(b) for b in espnowex.get_mac()])
    """

    # TODO add some error handling
    wlan_mac = wlan_sta.config('mac')
    
    return wlan_mac


def esp_tx(e, msg):
    print("start esp_tx")

    # # MAC address of peer1's wifi interface exmaple:
    # # peer1 = b'\xe8\x68\xe7\x4e\xbb\x19'
    # the receiver MAC address
    # peer = b'\x8c\xaa\xb5M\x7f\x18'  # my #2 esp8266
    peer = b'\xec\xfa\xbc\xcb\xab\xce' 

    print("Starting...")            # Send to all peers
    try:
        res = e.send(peer, msg, True)  # transmit data and check receive status
        if not res:
            print(f"DATA NOT RECORDED response:{res}")
        else:
            print(f"DATA TX SUCCESSFUL response:{res}")

    except OSError as err:
        if err.args[0] == errno.ETIMEDOUT:  # standard timeout is okay, ignore it
            print("ETIMEDOUT found")  # timeout is okay, ignore it
        else:  # general case, close the socket and continue processing, prevent hanging
            print(f"ERROR: {err}")

    print("done exp_tx")
    return res


def esp_rx(esp_con):
    """init of esp connection needs performed first
    peers need to be added to the espnow connection"""

    # wait for a message to process
    # while True:
    host, msg = esp_con.recv()
    # TODO change this to trap for errors, no need to check the msg
    if msg:
        if msg == b'get_time':
            # send time to sender
            print("host: {host} requested time")
        else:
            print(f"received from: {host}, message: {msg}")
    
    return host, msg
                
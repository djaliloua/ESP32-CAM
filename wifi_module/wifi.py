import ujson as json
from time import sleep
import network
import os
import _thread as threading
from wifi_module.wifimngr import WifiMngr

file_name = "wifi.json"

def read_wifi_json():
    if file_name in os.listdir():
        with open(file_name, "r") as file:
            data = file.read()
            #print(data)
            d = json.loads(data)
            return dict(d)
    return None


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        data = read_wifi_json()
        #print(data)
        if data:
            try:
                wlan.connect(data["ssid"], data["password"]) # ('DIGIFIBRA-5FA8', '8CU8FN8Y34')
                while not wlan.isconnected():
                    pass
            except OSError as e:
                wlan.active(False)
                wifi = WifiMngr()
                wifi.start_server()
                return wifi.ip_address 
            
        else:
            wlan.active(False)
            wifi = WifiMngr()
            wifi.start_server()
            return wifi.ip_address
    print('network config:', wlan.ifconfig())
    return wlan.ifconfig()[0]


#do_connect()





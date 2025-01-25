import network
import socket
import os
import ujson as json
import _thread as threading
import re
import time


lock = threading.allocate_lock()

class WifiMngr:
    def __init__(self, ssid="ESP_Connect", password="123456789", port=80):
        self.wlan = network.WLAN(network.STA_IF) # create station interface
        self.ap = network.WLAN(network.AP_IF)
        self.ssid = ssid
        self.password = password
        self.host = self.create_access_point()
        self.port = port
        self.ip_address = None
        self.file_name = "wifi.json"
        self.close_ap = False
        
    def disactivate(self):
        time.sleep(2)
        self.ap.active(False)
        self.server_socket.close()
        
        
    def create_access_point(self):
        if self.ap.active():
            print("Access point already active!")
            print("SSID: ", self.ap.config("essid"))
            print("IP Address:", self.ap.ifconfig()[0])  # Get the IP address
            return self.ap.ifconfig()[0]
        
        self.ap.active(True)
        self.ap.config(essid=self.ssid, password=self.password, authmode=network.AUTH_WPA_WPA2_PSK)
        print("Access Point Configured:", self.ssid)
        print("IP:", self.ap.ifconfig()[0])
        # start server
        
        return self.ap.ifconfig()[0]
    
    def read_wifi_json(self):
        if self.file_name in os.listdir():
            with open(self.file_name, "r") as file:
                data = file.read()
                d = json.loads(data)
                return dict(d)
        return None
        
    def scan_wifi(self):
        self.wlan.active(True)       # activate the interface
        list_of_wifi = self.wlan.scan()
        self.wlan.active(False)
        return [x[0].decode() for x in list_of_wifi]
 
    def handle_client(self, conn, addr):
        with lock:
            request = conn.recv(1024).decode()
            print(f"Received request from {addr}:\n{request}")

            # Serve the HTML file if requested
            if "GET / " in request or "GET /wifi_mqtt.html " in request:
                with open("wifi_module/wifi_mqtt.html", "r") as file:
                    content = file.read()
                response = 'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\nAccess-Control-Allow-Methods: GET, POST, OPTIONS \nContent-Type: text/html\n\n' + content
                conn.sendall(response.encode())

            # Handle AJAX request http://192.168.4.1/
            elif "GET /ready" in request:
                response_data = f"{json.dumps(self.scan_wifi())}"
                response = 'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\nAccess-Control-Allow-Methods: GET, POST, OPTIONS \nContent-Type: application/json\n\n' + response_data
                conn.sendall(response.encode())
     
            elif "POST /submit" in request:
                pattern = re.search(r'\{.*\}', request)
                if pattern:
                    #print(pattern.group(0))
                    with open("wifi.json", "w") as file:
                        file.write(pattern.group(0))
                        data = json.loads(pattern.group(0))
                        ip = self.connect_wifi(dict(data))
                        response_data = json.dumps({"message": f"http://{ip}:8080"})
                        response = 'HTTP/1.1 200 OK\nAccess-Control-Allow-Origin: *\nAccess-Control-Allow-Methods: GET, POST, OPTIONS \nContent-Type: application/json\n\n' + response_data
                        conn.sendall(response.encode())
                        time.sleep(1)
                        self.close_ap = True
                        print("Closing AP222: ", self.close_ap)
                        

            # Default response for other requests
            else:
                response = 'HTTP/1.1 404 Not Found\n\n'
                conn.sendall(response.encode())

            conn.close()
        
    def connect_wifi(self, data):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(data["ssid"], data["password"]) # ('DIGIFIBRA-5FA8', '8CU8FN8Y34')
            while not wlan.isconnected():
                pass
        print('network config:', wlan.ifconfig())
        self.ip_address = wlan.ifconfig()[0]
        return wlan.ifconfig()[0]
    
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        while not self.close_ap:
            conn, addr = self.server_socket.accept()
            self.handle_client(conn, addr)
            
        self.disactivate()
           
            

        
if __name__ == "__main__":
    pass
    #wifi = WifiMngr()
    #wifi.start_server()
        



import time
from umqtt.simple import MQTTClient
import machine
from machine import Pin
import esp
import urequests
import camera  # ESP32-CAM specific
#from wifi_module.wifi import do_connect, read_wifi_json
from camera_module.camera_handlers import CameraHandler
import asyncio
from update_service.model import MQTTConfig


is_connected = False
flash = Pin(4, Pin.OUT)

# MQTT Config
MQTT_PORT = 1883
CLIENT_ID = "esp32_camera"
MQTT_PASSWORD = "801490"
MQTT_USERNAME = "your_username"


def init_camera():
    camera.init(0, format=camera.JPEG)
    camera.framesize(camera.FRAME_VGA)  # Options: FRAME_96X96, FRAME_QQVGA, FRAME_VGA, etc.
    camera.flip(0)
    camera.mirror(0)
    print("Camera initialized")
    
def capture_image():
    #print("Capturing image...")
    img = camera.capture()
    #print(f"Captured image size: {len(img)} bytes")
    return img

def publish_image(client, topic, image):
    #print("Publishing image...")
    client.publish(topic, image)
    #print("Image published to topic:", topic)

async def start_streaming_video(mqttConfig):
    #connect_to_wifi()
    global is_connected
    #do_connect()
    #data = read_wifi_json()
    MQTT_BROKER = mqttConfig.hostName
    MQTT_TOPIC = mqttConfig.baseTopicName
    
    # handlers
    handlers = CameraHandler(camera, MQTT_TOPIC, flash)
    
    # Init camera
    init_camera()

    client = MQTTClient(client_id=mqttConfig.name,
                        server=MQTT_BROKER,
                        port=mqttConfig.port,
                        user=mqttConfig.userName,
                        password=mqttConfig.password)
    while True:
        try:
            client.connect()
            is_connected = True
            print("Connected to MQTT broker")
            # Subscribe to flash control topic
            # Set Handlers
            client.set_callback(handlers.on_message)
            
            # Sub
            client.subscribe(handlers.MQTT_FLASH_TOPIC)
            client.subscribe(handlers.MQTT_FLIP_TOPIC)
            client.subscribe(handlers.MQTT_MIRROR_TOPIC)
            client.subscribe(handlers.MQTT_SATURATION_TOPIC)
            client.subscribe(handlers.MQTT_BRIGHTNESS_TOPIC)
            client.subscribe(handlers.MQTT_CONTRAST_TOPIC)
            client.subscribe(handlers.MQTT_QUALITY_TOPIC)
            #client.subscribe(handlers.MQTT_MIRROR_TOPIC)
            while True:
                try:
                    img = capture_image()
                    publish_image(client, MQTT_TOPIC, img)
                    client.check_msg() # Check for new messages and call on_message_flash
                    await asyncio.sleep(0.1)  # Publish every 10 seconds
                except OSError as e:
                    print("hello world")
                    is_connected = False
                    break
                
        except KeyboardInterrupt:
            print("Exiting...")
            
        except OSError as e:
            pass

        finally:
            if is_connected:
                client.disconnect()
                camera.deinit()
                print("Disconnected and camera deinitialized")



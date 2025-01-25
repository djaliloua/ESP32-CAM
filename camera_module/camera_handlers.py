class CameraHandler:
    def __init__(self, cam, topic, flash):
        self.camera = cam
        self.flash = flash
        self.MQTT_TOPIC = topic
        self.MQTT_FLASH_TOPIC = f"camera/{self.MQTT_TOPIC.split("/")[-1]}/flash"
        self.MQTT_FLIP_TOPIC = f"camera/{self.MQTT_TOPIC.split("/")[-1]}/flip"
        self.MQTT_MIRROR_TOPIC = f"camera/{self.MQTT_TOPIC.split("/")[-1]}/mirror"
        self.MQTT_SATURATION_TOPIC = f"camera/{self.MQTT_TOPIC.split("/")[-1]}/saturation"
        self.MQTT_BRIGHTNESS_TOPIC = f"camera/{self.MQTT_TOPIC.split("/")[-1]}/brightness"
        self.MQTT_CONTRAST_TOPIC = f"camera/{self.MQTT_TOPIC.split("/")[-1]}/contrast"
        self.MQTT_QUALITY_TOPIC = f"camera/{self.MQTT_TOPIC.split("/")[-1]}/quality"
        
        
    def on_message(self, topic, msg):
        print("Received message on topic", topic, ": ", msg.decode())
        topic_head = self._get_topic_head(topic.decode())
        if topic_head == "mirror":
            if msg.decode() == "ON":
                self.camera.mirror(1)
            elif msg.decode() == "OFF":
                self.camera.mirror(0)
            return
        
        if topic_head == "flip":
            if msg.decode() == "ON":
                self.camera.flip(1)
            elif msg.decode() == "OFF":
                self.camera.flip(0)
            return
        
        if topic_head == "flash":
            if msg.decode() == "ON":
                self.flash.on()
            elif msg.decode() == "OFF":
                self.flash.off()
            return
        
        if topic_head == "saturation":
            self.camera.saturation(int(msg.decode()))
            return
        
        if topic_head == "brightness":
            self.camera.brightness(int(msg.decode()))
            return
        
        if topic_head == "contrast":
            self.camera.contrast(int(msg.decode()))
            return
        
        if topic_head == "quality":
            self.camera.quality(int(msg.decode()))
            return
        
 
    def _get_topic_head(self, topic):
        return topic.split("/")[-1]
        

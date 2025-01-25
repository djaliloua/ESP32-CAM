import json
import os



class MQTTConfig:
    def __init__(self, cameraId, name, hostName, port, username, password, baseTopicName, isActive, id):
        self.cameraId = cameraId
        self.name = name
        self.hostName = hostName
        self.port = port
        self.userName = username
        self.password = password
        self.baseTopicName = baseTopicName
        self.isActive = isActive
        self.id = id
        
    def to_dictionary(self):
        return self.__dict__

    @staticmethod
    def from_dict(data_str):
        obj = json.loads(data_str)
        _cameraId = str(obj.get("cameraId"))
        _name = str(obj.get("name"))
        _hostName = str(obj.get("hostName"))
        _port = str(obj.get("port"))
        _userName = str(obj.get("userName"))
        _password = str(obj.get("password"))
        _baseTopicName = str(obj.get("baseTopicName"))
        _isActive = bool(obj.get("isActive"))
        _id = int(obj.get("id"))
        return MQTTConfig(_cameraId, _name, _hostName, _port, _userName, _password, _baseTopicName, _isActive, _id)
    
    @staticmethod
    def load_from_json(filename="mqttconfig.json"):
        config = MQTTConfig("", "", "", "", "", "", "", False, 0)
        if filename in os.listdir():
            with open(filename, "r") as f:
                config = MQTTConfig.from_dict(f.read())
        return config
    
    def save_to_json(self, filename="mqttconfig.json"):
        with open(filename, "w") as f:
            f.write(json.dumps(self.to_dictionary()))
            
    def __eq__(self, other):
        if not isinstance(other, MQTTConfig):
            return False
        # Compare the relevant attributes of the objects
        return self.password == other.password and self.userName == other.userName and self.baseTopicName == other.baseTopicName and self.port == other.port and self.name == other.name
            
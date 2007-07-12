import os

class OwSettings:
    def __init__(self):
        self.owfsRoot = ""

class OwSensor:
    
    def __init__(self, owfsSettings, sensorPath):
        #if owfsSettings.owfsRoot == "":
        #    raise RuntimeError, "You must set OWFS_ROOT to the owfs mount point."
        if not os.path.exists(sensorPath):
            raise RuntimeError, "Sensor does not exist."
        if sensorPath[-1] != "/":
            sensorPath = sensorPath + "/"
        if not os.path.exists(sensorPath + "address"):
            raise RuntimeError, "Path does not seem to point to a valid sensor."
        self.__dict__["sensorPath"] = sensorPath
    
    def __getattr__(self, name):
        if os.path.exists(self.sensorPath + name):
            attr = open(self.sensorPath + name, "r")
            try:
                value = attr.read().strip()
            finally:
                attr.close()
            return value
        raise AttributeError, name
    
    def __setattr__(self, name, value):
        if os.path.exists(self.sensorPath + name):
            attr = open(self.sensorPath + name, "w")
            try:
                attr.write(value)
            finally:
                attr.close()
        else:
            self.__dict__[name] = value
    
class TemperatureSensor(OwSensor):
    
    def getTemperature(self):
        return float(self.__getattr__("temperature"))
    
class RelaySensor(OwSensor):
    
    def isOpen(self):
        pio = self.PIO
        return pio == "1"
    
    def close(self):
        if self.isOpen():
            self.PIO = "0"
            
    def open(self):
        if not self.isOpen():
            self.PIO = "1"
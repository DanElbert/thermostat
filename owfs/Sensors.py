import os
import re

class OwSettings:
    def __init__(self, owfsRoot):
        if owfsRoot == "" or owfsRoot == None:
            raise RuntimeError, "owfsRoot can not be null or empty."
        
        if owfsRoot[-1] != "/":
            owfsRoot = owfsRoot + "/"
        
        if not os.path.exists(owfsRoot):
            raise RuntimeError, "owfsRoot mount point does not exist."
        
        if not (os.path.exists(owfsRoot + "uncached/") and os.path.exists(owfsRoot + "bus.0/")):
            raise RuntimeError, "owfsRoot must be the root of an owfs mount point."
        self.owfsRoot = owfsRoot
        self.useCache = False

class OwSensor(object):
    
    def __init__(self, owfsSettings, sensorPath):
        
        if re.match(r'\d{2,2}\.[0-9a-fA-F]{12,12}/?', sensorPath) == None:
            raise RuntimeError, "(" + sensorPath + ") is not a valid sensor of the form XX.XXXXXXXXXXXX"
        
        if sensorPath[-1] != "/":
            sensorPath = sensorPath + "/"
            
        self.__sensorPath = sensorPath
        self.__owfsRoot = owfsSettings.owfsRoot
        self.useCache = owfsSettings.useCache
        
        if not os.path.exists(self.__getFullSensorPath()):
            raise RuntimeError, "Sensor does not exist."
        
        if self.address[2:-2] != sensorPath[3:-1]:
            raise RuntimeError, "sensorPath does not seem to point to a valid sensor.  The path (" + sensorPath[3:-1] + ") differs from the address attribute (" + self.address[2:-2] + ")."
        
    def __getFullSensorPath(self):
        if self.useCache:
            return self.__owfsRoot + "uncached/" + self.__sensorPath
        else:
            return self.__owfsRoot + self.__sensorPath
        
    def __getFullAttributePath(self, attributeName):
        return self.__getFullSensorPath() + attributeName
        
    def setAttribute(self, name, value):
        path = self.__getFullAttributePath(name)
        if os.path.exists(path):
            attr = open(path, "w")
            try:
                attr.write(value)
            except IOError:
                print "Error Writing to attribute %s" % name
                raise
            finally:
                attr.close()
        else:
            raise RuntimeError, "No such attribute %s in Sensor %s" % name, self.getFullSensorPath()
        
    def getAttribute(self, name):
        path = self.__getFullAttributePath(name)
        if os.path.exists(path):
            attr = open(path, "r")
            try:
                value = attr.read().strip()
            except IOError:
                print "Error reading attribute %s" % name
                raise
            finally:
                attr.close()
                
            return value
        else:
            raise RuntimeError, "No such attribute %s in Sensor %s" % name, self.getFullSensorPath()
        
    def __setaddress(self, value):
        self.setAttribute("address", value)
        
    def __getaddress(self):
        return self.getAttribute("address")
    
    address = property(__getaddress, __setaddress)
    
    def __setuseCache(self, value):
        self.__useCache = value
        
    def __getuseCache(self):
        return self.__useCache
    
    useCache = property(__getuseCache, __setuseCache)
    
class TemperatureSensor(OwSensor):
    
    def __gettemperature(self):
        return float(self.getAttribute("temperature"))
    
    temperature = property(__gettemperature)
    
class RelaySensor(OwSensor):
    
    def __getisOpen(self):
        pio = self.getAttribute("PIO")
        return pio == "1"
    
    isOpen = property(__getisOpen)
    
    def close(self):
        if self.isOpen:
            self.setAttribute("PIO", "0")
            
    def open(self):
        if not self.isOpen:
            self.setAttribute("PIO", "1")
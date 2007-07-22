import os
import re

class OwSettings:
    """
    Class to wrap some default parameters for accessing the 1 wire file system
    owfsRoot: points at the rool of the owfs mount point
    useCache: whether to use the built-in owfs caching mechanism or not
    """
    def __init__(self, owfsRoot, useCache = True):
        if owfsRoot == "" or owfsRoot == None:
            raise RuntimeError, "owfsRoot can not be null or empty."
        
        if owfsRoot[-1] != "/":
            owfsRoot = owfsRoot + "/"
        
        if not os.path.exists(owfsRoot):
            raise RuntimeError, "owfsRoot mount point does not exist."
        
        if not (os.path.exists(owfsRoot + "uncached/") and os.path.exists(owfsRoot + "bus.0/")):
            raise RuntimeError, "owfsRoot must be the root of an owfs mount point."
        self.owfsRoot = owfsRoot
        self.useCache = useCache

class OwSensor(object):
    """
    Base class for accessing a single sensor in the 1 wire network.
    """
    def __init__(self, owfsSettings, sensorPath):
        
        # ensure the sensor is of the correct form
        if re.match(r'\d{2,2}\.[0-9a-fA-F]{12,12}/?', sensorPath) == None:
            raise RuntimeError, "(" + sensorPath + ") is not a valid sensor of the form XX.XXXXXXXXXXXX"
        
        if sensorPath[-1] != "/":
            sensorPath = sensorPath + "/"
            
        self.__sensorPath = sensorPath
        self.__owfsRoot = owfsSettings.owfsRoot
        self.useCache = owfsSettings.useCache
        
        if not os.path.exists(self.__getFullSensorPath()):
            raise RuntimeError, "Sensor does not exist."
        
        # Ensure that the sensor path matches the id property of the sensor
        if self.id != sensorPath[3:-1]:
            raise RuntimeError, "sensorPath does not seem to point to a valid sensor.  The path (" + sensorPath[3:-1] + ") differs from the id attribute (" + self.id + ")."
        
    def __getFullSensorPath(self):
        "Returns the path to the sensor directory"
        if not self.useCache:
            return self.__owfsRoot + "uncached/" + self.__sensorPath
        else:
            return self.__owfsRoot + self.__sensorPath
        
    def __getFullAttributePath(self, attributeName):
        "Returns the path to the file for the given attribute"
        return self.__getFullSensorPath() + attributeName
        
    def setAttribute(self, name, value):
        "Writes the given value to the attribute file with the given name"
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
        "Returns the contents of the given attribute file"
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
            raise RuntimeError, "No such attribute " + name + " in Sensor " + self.__getFullSensorPath()
        
    def __getaddress(self):
        "address property getter"
        return self.getAttribute("address")
    
    address = property(__getaddress)
        
    def __getid(self):
        "id property getter"
        return self.getAttribute("id")
    
    id = property(__getid)
    
    def __setuseCache(self, value):
        "useCache property setter"
        self.__useCache = value
        
    def __getuseCache(self):
        "useCache property getter"
        return self.__useCache
    
    useCache = property(__getuseCache, __setuseCache)
    
class TemperatureSensor(OwSensor):
    """
    Class to represent a temperature sensor (DS18S20).
    Includes a temperature property that reads the temp and returns a float
    """
    def __gettemperature(self):
        return float(self.getAttribute("temperature"))
    
    temperature = property(__gettemperature)
    
class RelaySensor(OwSensor):
    """
    Class to represent a 1 wire network branch controller (DS2405)
    However, in this case, it is assumed the chip is controlling a relay.
    This class has a property to determine if the relay is open or closed,
    and includes methods for closing or opening the relay
    """
    
    def __getisOpen(self):
        pio = self.getAttribute("PIO")
        return pio == "1"
    
    isOpen = property(__getisOpen)
    
    def close(self):
        "Ensures the relay is closed"
        if self.isOpen:
            self.setAttribute("PIO", "0")
            
    def open(self):
        "Ensures the relay is open"
        if not self.isOpen:
            self.setAttribute("PIO", "1")
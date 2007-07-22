import Config
import unittest
import thermostatIO

class baseTestFixture(unittest.TestCase):
    def writeValue(self, deviceId, propertyName, value):
        if deviceId[-1] != "/":
            deviceId = deviceId + "/"
            
        root = Config.OWFS_MOUNT_ROOT
        if root[-1] != "/":
            root = root + "/"
            
        path = root + deviceId + propertyName
        try:
            file = open(path, "w")
            file.write(value)
        finally:
            if file != None:
                file.close()
                
    def disabletestWriteValue(self):
        io = thermostatIO.IO(True)
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "42")
        self.assertEqual(42.0, io.getAirTemperature())
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "24.89")
        self.assertEqual(24.89, io.getAirTemperature())
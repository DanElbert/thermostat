import Config
import unittest
import thermostatIO

class ioTestFixture(unittest.TestCase):
    
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
        
    def testInitialization(self):
        io = thermostatIO.IO(True)
        
        self.assertEqual("1234567890AB", io.airTemperatureSensor.id)
        self.assertEqual("234567890AB1", io.liquidTemperatureSensor.id)
        self.assertEqual("34567890AB12", io.ambientTemperatureSensor.id)
        self.assertEqual("4567890AB123", io.coolerSwitch.id)
        self.assertEqual("567890AB1234", io.heaterSwitch.id)
        
    def testWriteValue(self):
        io = thermostatIO.IO(True)
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "42")
        self.assertEqual(42.0, io.getAirTemperature())
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "24.89")
        self.assertEqual(24.89, io.getAirTemperature())
        
    def testTemperatureStatus(self):
        pass
from owfs import Sensors
import unittest

class owSensorTestFixture(unittest.TestCase):
    
    def setUp(self):
        self.owSettings = Sensors.OwSettings("/home/dan/development/thermostat/tests/fakeOwfsMount/")
    
    def testOwSensor(self):
        sensor = Sensors.OwSensor(self.owSettings, "01.1234567890AB")
        self.assertEqual("011234567890ABFF", sensor.address)
        
        sensor = Sensors.OwSensor(self.owSettings, "01.1234567890AB/")
        self.assertEqual("011234567890ABFF", sensor.address)
        self.assertEqual("1234567890AB", sensor.id)
        
        # In the fake mount point, the uncached version of the sensor has 'FAKE!' as the address.
        # This asserts that changing the useCache attribute changes the internal path of the sensor.
        sensor.useCache = False        
        self.assertEqual("FAKE!", sensor.address)
        
        sensor.useCache = True
        self.assertEqual("011234567890ABFF", sensor.address)
        
    def testTempSensor(self):
        file = open(self.owSettings.owfsRoot + "01.1234567890AB/temperature", "w")
        file.write("24.432")
        file.close()
        temp = Sensors.TemperatureSensor(self.owSettings, "01.1234567890AB")
        tempReading = temp.temperature
        self.assertEqual(24.432, tempReading)
        
    def testRelaySensor(self):
        file = open(self.owSettings.owfsRoot + "01.1234567890AB/PIO", "w")
        file.write("0")
        file.close()
        relay = Sensors.RelaySensor(self.owSettings, "01.1234567890AB")
        self.assertEqual(False, relay.isOpen)
        
        file = open(self.owSettings.owfsRoot + "01.1234567890AB/PIO", "w")
        file.write("1")
        file.close()
        
        self.assertEqual(True, relay.isOpen)
        relay.close()
        self.assertEqual(False, relay.isOpen)
        relay.close()
        self.assertEqual(False, relay.isOpen)
        
        file = open(self.owSettings.owfsRoot + "01.1234567890AB/PIO", "r")
        currVal = file.read()
        file.close()
        self.assertEqual("0", currVal)
        
        relay.open()
        self.assertEqual(True, relay.isOpen)
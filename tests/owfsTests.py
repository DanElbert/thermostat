from owfs import Sensors
import unittest

class owSensorTestFixture(unittest.TestCase):
    
    def setUp(self):
        self.owSettings = Sensors.OwSettings()
        self.owSettings.owfsRoot = "~/development/thermostat/tests/fakeOwfsMount/"
    
    def testOwSensor(self):
        sensor = Sensors.OwSensor(self.owSettings, "/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890")
        self.assertEqual("1234567890", sensor.address)
        
    def testTempSensor(self):
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890/temperature", "w")
        file.write("24.432")
        file.close()
        temp = Sensors.TemperatureSensor(self.owSettings, "/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890")
        tempReading = temp.getTemperature()
        self.assertEqual(24.432, tempReading)
        
    def testRelaySensor(self):
        pass
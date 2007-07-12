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
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890/PIO", "w")
        file.write("0")
        file.close()
        relay = Sensors.RelaySensor(self.owSettings, "/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890")
        self.assertEqual(False, relay.isOpen())
        
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890/PIO", "w")
        file.write("1")
        file.close()
        
        self.assertEqual(True, relay.isOpen())
        relay.close()
        self.assertEqual(False, relay.isOpen())
        relay.close()
        self.assertEqual(False, relay.isOpen())
        
        relay.open()
        self.assertEqual(True, relay.isOpen())
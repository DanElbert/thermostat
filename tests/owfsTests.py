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
        
    def testTempSensor(self):
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890AB/temperature", "w")
        file.write("24.432")
        file.close()
        temp = Sensors.TemperatureSensor(self.owSettings, "01.1234567890AB")
        tempReading = temp.temperature
        self.assertEqual(24.432, tempReading)
        
    def testRelaySensor(self):
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890AB/PIO", "w")
        file.write("0")
        file.close()
        relay = Sensors.RelaySensor(self.owSettings, "01.1234567890AB")
        self.assertEqual(False, relay.isOpen)
        
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890AB/PIO", "w")
        file.write("1")
        file.close()
        
        self.assertEqual(True, relay.isOpen)
        relay.close()
        self.assertEqual(False, relay.isOpen)
        relay.close()
        self.assertEqual(False, relay.isOpen)
        
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.1234567890AB/PIO", "r")
        currVal = file.read()
        file.close()
        self.assertEqual("0", currVal)
        
        relay.open()
        self.assertEqual(True, relay.isOpen)
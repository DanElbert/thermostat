from owfs import Sensors
import unittest

class owSensorTestFixture(unittest.TestCase):
    
    def setUp(self):
        self.owSettings = Sensors.OwSettings("/home/dan/development/thermostat/tests/fakeOwfsMount/")
    
    def testOwSensor(self):
        sensor = Sensors.OwSensor(self.owSettings, "01.123456789012")
        self.assertEqual("123456789012", sensor.address)
        
        sensor = Sensors.OwSensor(self.owSettings, "01.123456789012/")
        self.assertEqual("123456789012", sensor.address)
        
    def testTempSensor(self):
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.123456789012/temperature", "w")
        file.write("24.432")
        file.close()
        temp = Sensors.TemperatureSensor(self.owSettings, "01.123456789012")
        tempReading = temp.temperature
        self.assertEqual(24.432, tempReading)
        
    def testRelaySensor(self):
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.123456789012/PIO", "w")
        file.write("0")
        file.close()
        relay = Sensors.RelaySensor(self.owSettings, "01.123456789012")
        self.assertEqual(False, relay.isOpen)
        
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.123456789012/PIO", "w")
        file.write("1")
        file.close()
        
        self.assertEqual(True, relay.isOpen)
        relay.close()
        self.assertEqual(False, relay.isOpen)
        relay.close()
        self.assertEqual(False, relay.isOpen)
        
        file = open("/home/dan/development/thermostat/tests/fakeOwfsMount/01.123456789012/PIO", "r")
        currVal = file.read()
        file.close()
        self.assertEqual("0", currVal)
        
        relay.open()
        self.assertEqual(True, relay.isOpen)
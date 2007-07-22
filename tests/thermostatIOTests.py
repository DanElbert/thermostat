import Config
import datetime
import unittest
import thermostatIO
import time
from tests.TestUtils import *

class ioTestFixture(baseTestFixture):
         
    def testInitialization(self):
        io = thermostatIO.IO(True)
        
        self.assertEqual("1234567890AB", io.airTemperatureSensor.id)
        self.assertEqual("234567890AB1", io.liquidTemperatureSensor.id)
        self.assertEqual("34567890AB12", io.ambientTemperatureSensor.id)
        self.assertEqual("4567890AB123", io.coolerSwitch.id)
        self.assertEqual("567890AB1234", io.heaterSwitch.id)
        
        self.assertEqual(24.5, io.targetTemperature)
        self.assertEqual(1.5, io.maxTemperatureDelta)
        
        self.assertEqual(datetime.timedelta(seconds=.25), io.switchDelay)
        self.assertEqual(datetime.datetime.min, io.lastCoolerSwitch)
        self.assertEqual(datetime.datetime.min, io.lastHeaterSwitch)
        
    def testLastSwitch(self):
        io = thermostatIO.IO(True)
        
        self.writeValue(Config.COOLER_RELAY, "PIO", "0")
        self.writeValue(Config.HEATER_RELAY, "PIO", "1")
        self.assertEqual(datetime.timedelta(seconds=.25), io.switchDelay)
        
        self.assertEqual(datetime.datetime.min, io.lastCoolerSwitch)
        io.activateCooler()
        self.assert_((datetime.datetime.now() - io.lastCoolerSwitch) < datetime.timedelta(seconds=.1))
        self.failIf(io.hasCoolerSwitchDeltaPassed())
        
        self.assertEqual(datetime.datetime.min, io.lastHeaterSwitch)
        io.deactivateHeater()
        self.assert_((datetime.datetime.now() - io.lastHeaterSwitch) < datetime.timedelta(seconds=.1))
        self.failIf(io.hasHeaterSwitchDeltaPassed())
        
        time.sleep(.3)
        
        self.assert_(io.hasCoolerSwitchDeltaPassed())
        self.assert_(io.hasHeaterSwitchDeltaPassed())
        
    def testDelayExceptions(self):
        io = thermostatIO.IO(True)
        
        self.writeValue(Config.COOLER_RELAY, "PIO", "0")
        self.writeValue(Config.HEATER_RELAY, "PIO", "1")
        self.assertEqual(datetime.timedelta(seconds=.25), io.switchDelay)
        
        io.activateCooler()
        io.activateHeater()
        
        try:
            io.deactivateCooler()
            self.fail("deactivateCooler should have raised an error.")
        except:
            pass
        
        io.deactivateHeater()
        
        try:
            io.activateHeater()
            self.fail("activateHeater should have raised an error.")
        except:
            pass
        
        time.sleep(.3)
        io.deactivateCooler()
        io.activateHeater()        
        
    def testTemperatureStatus(self):
        io = thermostatIO.IO(True)
        
        self.assertEqual(24.5, io.targetTemperature)
        self.assertEqual(1.5, io.maxTemperatureDelta)
        
        self.writeValue(Config.COOLER_RELAY, "PIO", "0")
        self.writeValue(Config.HEATER_RELAY, "PIO", "0")
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "24.6")
        self.assertEqual(thermostatIO.IO.TEMP_GOOD_HIGH, io.getTemperatureStatus())
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "24.5")
        self.assertEqual(thermostatIO.IO.TEMP_GOOD_LOW, io.getTemperatureStatus())
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "23.0")
        self.assertEqual(thermostatIO.IO.TEMP_GOOD_LOW, io.getTemperatureStatus())
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "26.0")
        self.assertEqual(thermostatIO.IO.TEMP_GOOD_HIGH, io.getTemperatureStatus())
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "22.5")
        self.assertEqual(thermostatIO.IO.TEMP_LOW, io.getTemperatureStatus())
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "26.1")
        self.assertEqual(thermostatIO.IO.TEMP_HIGH, io.getTemperatureStatus())
        
import Config
from stateMachine import States
import thermostatIO
import unittest
from tests.TestUtils import *
import time

class testIdleState(baseTestFixture):
    def setUp(self):
        self.io = thermostatIO.IO(True)
        self.assertEqual(24.5, self.io.targetTemperature)
        self.assertEqual(1.5, self.io.maxTemperatureDelta)
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "24.5")
        self.writeValue(Config.COOLER_RELAY, "PIO", "0")
        self.writeValue(Config.HEATER_RELAY, "PIO", "1")
    
    def testEntry(self):
        idle = States.Idle(self.io)
        self.assertEqual("Idle", idle.getName())
        
        idle.Entry()
        self.assertEqual(self.io.getIsHeaterOn(), False)
        
    def testChangeState(self):
        idle = States.Idle(self.io)
        idle.Entry()
        
        # Drop the temperature very quickly.  Idle should still return itself
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "5")
        newState = idle.UpdateState()
        self.assertEqual(newState, idle)
        
        time.sleep(.3)
        
        # Now, after a delay, state should change to heating.
        newState = idle.UpdateState()
        self.assertEqual("Heating", newState.getName())
        
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "26.4")
        
        newState = idle.UpdateState()
        self.assertEqual("Cooling", newState.getName())
    
class testHeatingState(baseTestFixture):
    def setUp(self):
        self.io = thermostatIO.IO(True)
        self.assertEqual(24.5, self.io.targetTemperature)
        self.assertEqual(1.5, self.io.maxTemperatureDelta)
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "24.5")
        self.writeValue(Config.COOLER_RELAY, "PIO", "0")
        self.writeValue(Config.HEATER_RELAY, "PIO", "0")
        
    def testEntry(self):
        heating = States.Heating(self.io)
        self.assertEqual("Heating", heating.getName())
        
        heating.Entry()
        self.assertEqual(self.io.getIsHeaterOn(), True)
        
    def testChangeState(self):
        heating = States.Heating(self.io)
        heating.Entry()
        
        # Raise the temperature very quickly.  heating should still return itself
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "50")
        newState = heating.UpdateState()
        self.assertEqual(newState, heating)
        
        time.sleep(.3)
        
        # Now, after a delay, state should change to idle.
        newState = heating.UpdateState()
        self.assertEqual("Idle", newState.getName())
        
class testCoolingState(baseTestFixture):
    def setUp(self):
        self.io = thermostatIO.IO(True)
        self.assertEqual(24.5, self.io.targetTemperature)
        self.assertEqual(1.5, self.io.maxTemperatureDelta)
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "24.5")
        self.writeValue(Config.COOLER_RELAY, "PIO", "0")
        self.writeValue(Config.HEATER_RELAY, "PIO", "0")
        
    def testEntry(self):
        cooling = States.Cooling(self.io)
        self.assertEqual("Cooling", cooling.getName())
        
        cooling.Entry()
        self.assertEqual(self.io.getIsCoolerOn(), True)
        
    def testChangeState(self):
        cooling = States.Cooling(self.io)
        cooling.Entry()
        
        # Drop the temperature very quickly.  cooling should still return itself
        self.writeValue(Config.AIR_TEMP_SENSOR, "temperature", "5")
        newState = cooling.UpdateState()
        self.assertEqual(newState, cooling)
        
        time.sleep(.3)
        
        # Now, after a delay, state should change to idle.
        newState = cooling.UpdateState()
        self.assertEqual("Idle", newState.getName())
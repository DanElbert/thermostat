import datetime
from owfs import Sensors
import Config

class IO:
    """
    This class provides a layer of abstractions between the actual hardware object model
    and the state machine.  It also implements some of the logic surrounding delays between
    relay switching and temperature state based on configuration
    """
    
    # The three states the temperature may be in    
    TEMP_HIGH = 0
    TEMP_GOOD_HIGH = 1
    TEMP_GOOD_LOW = 2
    TEMP_LOW = 3
    
    def __init__(self, useCache = False):
        settings = Sensors.OwSettings(Config.OWFS_MOUNT_ROOT, useCache)
        
        self.airTemperatureSensor = Sensors.TemperatureSensor(settings, Config.AIR_TEMP_SENSOR)
        self.ambientTemperatureSensor = Sensors.TemperatureSensor(settings, Config.AMBIENT_TEMPT_SENSOR)
        self.liquidTemperatureSensor = Sensors.TemperatureSensor(settings, Config.LIQUID_TEMP_SENSOR)
        
        self.coolerSwitch = Sensors.RelaySensor(settings, Config.COOLER_RELAY)
        self.heaterSwitch = Sensors.RelaySensor(settings, Config.HEATER_RELAY)
        
        self.targetTemperature = float(Config.TARGET_TEMPERATURE)
        self.maxTemperatureDelta = float(Config.MAX_TEMPERATURE_DELTA)
        self.switchDelay = datetime.timedelta(seconds = float(Config.SWITCH_DELAY))
        self.lastHeaterSwitch = datetime.datetime.min
        self.lastCoolerSwitch = datetime.datetime.min
        
    def getAirTemperature(self):
        """
        Returns the current air temperature of the fridge
        """
        return self.airTemperatureSensor.temperature
    
    def getAmbientTemperature(self):
        """
        Returns the current ambient temperature outside of the fridge
        """
        return self.ambientTemperatureSensor.temperature
    
    def getLiquidTemperature(self):
        """
        Returns the current temperature of the liquid inside the fridge
        """
        return self.liquidTemperatureSensor.temperature
    
    def getIsCoolerOn(self):
        """
        Whether or not the cooler is on
        """
        return self.coolerSwitch.isOpen
    
    def getIsHeaterOn(self):
        """
        Whether or not the heater is on
        """
        return self.heaterSwitch.isOpen
    
    def activateHeater(self):
        """
        If the Heater is off, this turns it on.
        Note that if the switch delay has not yet passed, this method throws an exception.
        """
        if not self.heaterSwitch.isOpen:
            if not self.hasHeaterSwitchDeltaPassed():
                raise RuntimeError, "Heater can not be activated so soon after being deactivated."
            self.lastHeaterSwitch = datetime.datetime.now()
            self.heaterSwitch.open()
        
    def deactivateHeater(self):
        """
        If the Heater is on, this turns it off.
        Note that if the switch delay has not yet passed, this method throws an exception.
        """
        if self.heaterSwitch.isOpen:
            if not self.hasHeaterSwitchDeltaPassed():
                raise RuntimeError, "Heater can not be deactivated so soon after being activated."
            self.lastHeaterSwitch = datetime.datetime.now()
            self.heaterSwitch.close()
        
    def activateCooler(self):
        """
        If the Cooler is off, this turns it on.
        Note that if the switch delay has not yet passed, this method throws an exception.
        """
        if not self.coolerSwitch.isOpen:
            if not self.hasCoolerSwitchDeltaPassed():
                raise RuntimeError, "Cooler can not be activated so soon after being deactivated."
            self.lastCoolerSwitch = datetime.datetime.now()
            self.coolerSwitch.open()
        
    def deactivateCooler(self):
        """
        If the Cooler is on, this turns it off.
        Note that if the switch delay has not yet passed, this method throws an exception.
        """
        if self.coolerSwitch.isOpen:
            if not self.hasCoolerSwitchDeltaPassed():
                raise RuntimeError, "Cooler can not be deactivated so soon after being activated."
            self.lastCoolerSwitch = datetime.datetime.now()
            self.coolerSwitch.close()
            
    def hasCoolerSwitchDeltaPassed(self):
        """
        Returns whether the relay delay has passed since the cooler switch was last changed.
        """
        if (datetime.datetime.now() - self.lastCoolerSwitch) < self.switchDelay:
            return False
        return True
    
    def hasHeaterSwitchDeltaPassed(self):
        """
        Returns whether the relay delay has passed since the heater switch was last changed.
        """
        if (datetime.datetime.now() - self.lastHeaterSwitch) < self.switchDelay:
            return False
        return True
        
    def getTemperatureStatus(self):
        """
        Determines and returns the appropriate temperature state for the state machine to make
        decisions
        """
        temp = self.airTemperatureSensor.temperature
        lowGood = self.targetTemperature - self.maxTemperatureDelta
        highGood = self.targetTemperature + self.maxTemperatureDelta
        
        if temp < lowGood:
            return IO.TEMP_LOW
        
        if temp > highGood:
            return IO.TEMP_HIGH
        
        if temp > self.targetTemperature:
            return IO.TEMP_GOOD_HIGH
        
        return IO.TEMP_GOOD_LOW
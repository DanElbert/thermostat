import datetime
from owfs import Sensors
import Config

class IO:
    
    TEMP_HIGH = 0
    TEMP_GOOD = 1
    TEMP_LOW = 2
    
    def __init__(self, useCache = False):
        settings = Sensors.OwSettings(Config.OWFS_MOUNT_ROOT, useCache)
        
        self.airTemperatureSensor = Sensors.TemperatureSensor(settings, Config.AIR_TEMP_SENSOR)
        self.ambientTemperatureSensor = Sensors.TemperatureSensor(settings, Config.AMBIENT_TEMPT_SENSOR)
        self.liquidTemperatureSensor = Sensors.TemperatureSensor(settings, Config.LIQUID_TEMP_SENSOR)
        
        self.coolerSwitch = Sensors.RelaySensor(settings, Config.COOLER_RELAY)
        self.heaterSwitch = Sensors.RelaySensor(settings, Config.HEATER_RELAY)
        
        self.switchDelay = datetime.timedelta(seconds = float(Config.SWITCH_DELAY))
        self.lastHeaterSwitch = datetime.datetime.min
        self.lastCoolerSwitch = datetime.datetime.min
        
    def getAirTemperature(self):
        return self.airTemperatureSensor.temperature
    
    def getAmbientTemperature(self):
        return self.ambientTemperatureSensor.temperature
    
    def getLiquidTemperature(self):
        return self.liquidTemperatureSensor.temperature
    
    def getIsCoolerOn(self):
        return self.coolerSwitch.isOpen
    
    def getIsHeaterOn(self):
        return self.heaterSwitch.isOpen
    
    def activateHeater(self):
        if not self.heaterSwitch.isOpen:
            self.lastHeaterSwitch = datetime.datetime.now()
            self.heaterSwitch.open()
        
    def deactivateHeater(self):
        if self.heaterSwitch.isOpen:
            self.lastHeaterSwitch = datetime.datetime.now()
            self.heaterSwitch.close()
        
    def activateCooler(self):
        if not self.coolerSwitch.isOpen():
            self.lastCoolerSwitch = datetime.datetime.now()
            self.coolerSwitch.open()
        
    def deactivateCooler(self):
        if self.coolerSwitch.isOpen():
            self.lastCoolerSwitch = datetime.datetime.now()
            self.coolerSwitch.close()
        
    def getTemperatureStatus(self):
        return TEMP_GOOD
    
    def hasCoolerSwitchDeltaPassed(self):
        if (datetime.datetime.now() - self.lastCoolerSwitch) < self.switchDelay:
            return False
        return True
    
    def hasHeaterSwitchDeltaPassed(self):
        if (datetime.datetime.now() - self.lastHeaterSwitch) < self.switchDelay:
            return False
        return True
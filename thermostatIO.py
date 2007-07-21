from owfs import Sensors
import Config
import sys
import io

class IO:
    
    TEMP_HIGH = 0
    TEMP_GOOD = 1
    TEMP_LOW = 2
    
    def __init__(self):
        settings = Sensors.OwSettings(Config.OWFS_MOUNT_ROOT, False)
        
        self.airTemperatureSensor = Sensors.TemperatureSensor(settings, Config.AIR_TEMP_SENSOR)
        self.ambientTemperatureSensor = Sensors.TemperatureSensor(settings, Config.AMBIENT_TEMPT_SENSOR)
        self.liquidTemperatureSensor = Sensors.TemperatureSensor(settings, Config.LIQUID_TEMP_SENSOR)
        self.coolerSwitch = Sensors.RelaySensor(settings, Config.COOLER_RELAY)
        self.heaterSwitch = Sensors.RelaySensor(settings, Config.HEATER_RELAY)
        
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
        self.heaterSwitch.open()
        
    def deactivateHeater(self):
        self.heaterSwitch.close()
        
    def activateCooler(self):
        self.coolerSwitch.open()
        
    def deactivateCooler(self):
        self.coolerSwitch.close()
        
    def getTemperatureStatus(self):
        return TEMP_GOOD
    
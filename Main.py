import time
import Config
from owfs import Sensors

settings = Sensors.OwSettings(Config.OWFS_MOUNT_ROOT)
settings.useCache = False

temp_sensor = Sensors.TemperatureSensor(settings, Config.AIR_TEMP_SENSOR)
switch_sensor = Sensors.RelaySensor(settings, Config.COOLER_RELAY)

print "Starting..."

while True:
    
    print "Current Temperature: " + str(temp_sensor.temperature)
    print "Is Switch Open     : " + str(switch_sensor.isOpen)
    
    if temp_sensor.temperature > float(Config.TARGET_TEMPERATURE):
        switch_sensor.open()
    else:
        switch_sensor.close()
        
    time.sleep(2)
import time
from owfs import Sensors

settings = Sensors.OwSettings
settings.owfsRoot = "junk"

temp_sensor = Sensors.TemperatureSensor(settings, "/media/owfs/uncached/10.382C4D010800/")
switch_sensor = Sensors.RelaySensor(settings, "/media/owfs/uncached/05.7C0A32000000/")

print "Starting..."

while True:
    
    print "Current Temperature: " + str(temp_sensor.getTemperature())
    print "Is Switch Open     : " + str(switch_sensor.isOpen())
    
    if temp_sensor.getTemperature() > 24.0:
        switch_sensor.open()
    else:
        switch_sensor.close()
        
    time.sleep(5)
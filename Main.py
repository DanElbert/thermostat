import time
from owfs import Sensors

settings = Sensors.OwSettings("/media/owfs/")

temp_sensor = Sensors.TemperatureSensor(settings, "10.382C4D010800/")
switch_sensor = Sensors.RelaySensor(settings, "05.7C0A32000000/")

print "Starting..."

while True:
    
    print "Current Temperature: " + str(temp_sensor.temperature)
    print "Is Switch Open     : " + str(switch_sensor.isOpen)
    
    if temp_sensor.temperature > 30.0:
        switch_sensor.open()
    else:
        switch_sensor.close()
        
    time.sleep(5)
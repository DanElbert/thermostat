from stateMachine import States
import Config
import os
import datetime

class SimplisticLogger(object):
    def __init__(self):
        self.file = Config.SIMPLE_LOGGER_PATH
        
    def log(self, state):
        file = open(self.file, "a")
        timeStr = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M")
        data = "%s -- State: %s   Temp: %s   Heater: %s   Cooler: %s\n" % (timeStr, state.getName(), state.IO.getAirTemperature(), state.IO.getIsHeaterOn(), state.IO.getIsCoolerOn())
        file.write(data)
        file.close()
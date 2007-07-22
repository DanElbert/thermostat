from stateMachine import States
import Config
import os

class SimplisticLogger(object):
    def __init__(self):
        self.file = Config.SIMPLE_LOGGER_PATH
        
    def log(self, state):
        file = open(self.file, "a")
        data = "State: %s   Temp: %s   Heater: %s   Cooler: %s\n" % (state.getName(), state.IO.getAirTemperature(), state.IO.getIsHeaterOn(), state.IO.getIsCoolerOn())
        file.write(data)
        file.close()
import thermostatIO

class State(object):
    def __init__(self, thermostatIO):
        self.IO = thermostatIO
        
    def Entry(self):
        raise RuntimeError, "Abstract State cannot be run."
    
    def EnsureState(self):
        return self
    
    def Exit(self):
        pass
    
    def getName(self):
        return "Abstract State.  Something's broken."

class Idle(State):
    
    def Entry(self):
        self.IO.deactivateHeater()
        self.IO.deactivateCooler()
        
    def EnsureState(self):
        
        status = self.IO.getTemperatureStatus()
        
        if status == thermostatIO.IO.TEMP_GOOD:
            return self
        elif status == thermostatIO.IO.TEMP_HIGH:
            return Cooling()
        elif status == thermostatIO.IO.TEMP_LOW:
            return Heating()
        
    def getName(self):
        return "Idle"
        
class Heating(State):
    
    def Entry(self):
        self.IO.deactivateCooler()
        self.IO.activateHeater()
    
    def EnsureState(self):
        status = self.IO.getTemperatureStatus()
        
        if status == thermostatIO.IO.TEMP_GOOD or status == thermostatIO.IO.TEMP_HIGH:
            return Idle()
        elif status == thermostatIO.IO.TEMP_LOW:
            return self
        
    def getName(self):
        return "Heating"
    
class Cooling(State):
    
    def Entry(self):
        self.IO.activateCooler()
        self.IO.deactivateHeater()
    
    def EnsureState(self):
        status = self.IO.getTemperatureStatus()
        
        if status == thermostatIO.IO.TEMP_GOOD or status == thermostatIO.IO.TEMP_LOW:
            return Idle()
        elif status == thermostatIO.IO.TEMP_HIGH:
            return self
        
    def getName(self):
        return "Cooling"
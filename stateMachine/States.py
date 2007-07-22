import thermostatIO

class State(object):
    def __init__(self, thermostatIO):
        self.IO = thermostatIO
        
    def Entry(self):
        raise RuntimeError, "Abstract State cannot be run."
    
    def UpdateState(self):
        return self
    
    def Exit(self):
        pass
    
    def getName(self):
        return "Abstract State.  Something's broken."

class Idle(State):
    
    def Entry(self):
        self.IO.deactivateHeater()
        self.IO.deactivateCooler()
        
    def UpdateState(self):
        
        status = self.IO.getTemperatureStatus()
        
        if status == thermostatIO.IO.TEMP_HIGH and self.IO.hasCoolerSwitchDeltaPassed():
            return Cooling(self.IO)
        elif status == thermostatIO.IO.TEMP_LOW and self.IO.hasHeaterSwitchDeltaPassed():
            return Heating(self.IO)
        
        return self
        
    def getName(self):
        return "Idle"
        
class Heating(State):
    
    def Entry(self):
        self.IO.deactivateCooler()
        self.IO.activateHeater()
    
    def UpdateState(self):
        status = self.IO.getTemperatureStatus()
        
        if (status == thermostatIO.IO.TEMP_GOOD_HIGH or status == thermostatIO.IO.TEMP_HIGH) and self.IO.hasHeaterSwitchDeltaPassed():
            return Idle(self.IO)
        
        return self
        
    def getName(self):
        return "Heating"
    
class Cooling(State):
    
    def Entry(self):
        self.IO.activateCooler()
        self.IO.deactivateHeater()
    
    def UpdateState(self):
        status = self.IO.getTemperatureStatus()
        
        if (status == thermostatIO.IO.TEMP_GOOD_LOW or status == thermostatIO.IO.TEMP_LOW) and self.IO.hasCoolerSwitchDeltaPassed():
            return Idle(self.IO)
        
        return self
        
    def getName(self):
        return "Cooling"
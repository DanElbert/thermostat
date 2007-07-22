import time
import Config
import Loggers
from stateMachine import Thermostat
from stateMachine import States
import thermostatIO


print "Starting..."

logger = Loggers.SimplisticLogger()
io = thermostatIO.IO()
idle = States.Idle(io)
machine = Thermostat.StateManager(idle, Config.STATE_MANAGER_DELAY, logger)

machine.run()
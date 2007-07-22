import ConfigParser
import os
import sys

path = sys.path[0]
if path[-1] != "/":
    path = path + "/"

config = ConfigParser.ConfigParser()
config.read(path + "config.ini")

AIR_TEMP_SENSOR = config.get("Sensors", "airtempid")
LIQUID_TEMP_SENSOR = config.get("Sensors", "liquidtempid")
AMBIENT_TEMPT_SENSOR = config.get("Sensors", "ambienttempid")
COOLER_RELAY = config.get("Sensors", "coolerswitchid")
HEATER_RELAY = config.get("Sensors", "heaterswitchid")
OWFS_MOUNT_ROOT = config.get("Sensors", "owfsmount")

TARGET_TEMPERATURE = config.get("Thermostat", "targettemp")
MAX_TEMPERATURE_DELTA = config.get("Thermostat", "maxtemperaturedelta")
SWITCH_DELAY = config.get("Thermostat", "switchdelay")
STATE_MANAGER_DELAY = config.get("Thermostat", "statemanagerdelay")

SIMPLE_LOGGER_PATH = config.get("Logging", "SimpleLoggerFile")
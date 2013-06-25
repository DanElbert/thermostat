
require 'pathname'

files = [
    'owfs_path_info',
    'config',
    'sensors/base',
    'sensors/relay_sensor',
    'sensors/temperature_sensor',
    'states/base',
    'states/cooling',
    'states/idle',
    'thermostat_io',
    'state_machine'
]

root_path = File.expand_path('../thermostat', __FILE__)
root_path += '/' if root_path[-1] != '/'
files.each { |f| require File.expand_path(root_path + f) }

module Thermostat
  VERSION = '0.0.1'
end
#!/usr/bin/env ruby

require File.expand_path('../../config/environment', __FILE__)

config = Thermostat::Config.load_from_file(THERMOSTAT_CONFIG)
io = Thermostat::ThermostatIO.new(config)
start_state = Thermostat::States::Idle.new(io)

state_machine = Thermostat::StateMachine.new(start_state, config)

state_machine.run
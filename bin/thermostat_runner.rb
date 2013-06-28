#!/usr/bin/env ruby

require File.expand_path('../../lib/thermostat', __FILE__)

config = Thermostat::Config.load
io = Thermostat::ThermostatIO.new(config)
start_state = Thermostat::States::Idle.new(io)

state_machine = Thermostat::StateMachine.new(start_state, config.state_manager_delay)

state_machine.run
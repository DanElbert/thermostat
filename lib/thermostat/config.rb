module Thermostat
  class Config

    attr_accessor :owfs_mount, :air_temperature_id, :cooler_relay_id, :heater_relay_id
    attr_accessor :target_temp, :switch_delay, :max_temperature_delta, :state_manager_delay

    def self.load
      config = Config.new

      config.owfs_mount = '/mnt/1wire/'
      config.air_temperature_id = '10.382C4D010800'
      config.cooler_relay_id = '05.7C0A32000000'
      config.heater_relay_id = '05.EF0932000000'

      # In degrees C
      config.target_temp = 32.0

      # In Seconds
      config.switch_delay = 15

      # In degrees C
      config.max_temperature_delta = 2

      # In seconds
      config.state_manager_delay = 30

      config
    end
  end
end
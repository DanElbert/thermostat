module Thermostat
  # This class provides a layer of abstractions between the actual hardware object model
  # and the state machine.  It also implements some of the logic surrounding delays between
  # relay switching and temperature state based on configuration
  class ThermostatIO
    # The four states the temperature may be in
    TEMP_HIGH = 0
    TEMP_GOOD_HIGH = 1
    TEMP_GOOD_LOW = 2
    TEMP_LOW = 3

    def initialize(config)
      path_info = OwfsPathInfo.new(config.owfs_mount, false)

      @air_temperature_sensor = Sensors::TemperatureSensor.new(path_info, config.air_temperature_id)
      @cooler_relay_sensor = Sensors::RelaySensor.new(path_info, config.cooler_relay_id)

      # Ensure all relays start turned off
      @cooler_relay_sensor.turn_off

      @target_temp = config.target_temp
      @switch_delay = config.switch_delay
      @max_temperature_delta = config.max_temperature_delta
      @last_cooler_switch = nil
    end

    def get_air_temperature
      @air_temperature_sensor.temperature
    end

    def cooler_on?
      @cooler_relay_sensor.on?
    end

    def activate_cooler
      unless cooler_on?
        raise "Cooler cannot be activated so soon after being deactivated" unless cooler_switch_delay_passed?

        @cooler_relay_sensor.turn_on
        @last_cooler_switch = Time.new
      end
    end

    def deactivate_cooler
      if cooler_on?
        raise "Cooler cannot be deactivated so soon after being activated" unless cooler_switch_delay_passed?

        @cooler_relay_sensor.turn_off
        @last_cooler_switch = Time.new
      end
    end

    def cooler_switch_delay_passed?
      @last_cooler_switch.nil? || ((Time.new - @last_cooler_switch) >= @switch_delay)
    end

    def get_temperature_status
      temp = get_air_temperature
      low_good = @target_temp - @max_temperature_delta
      high_good = @target_temp + @max_temperature_delta

      if temp < low_good
        ThermostatIO::TEMP_LOW
      elsif temp > high_good
        ThermostatIO::TEMP_HIGH
      elsif temp > @target_temp
        ThermostatIO::TEMP_GOOD_HIGH
      else
        ThermostatIO::TEMP_GOOD_LOW
      end

    end
  end
end
module Thermostat
  module Sensors
    # Class to represent a temperature sensor (DS18S20).
    # Includes a temperature method that reads the temp and returns a float
    class TemperatureSensor < Sensors::Base
      def temperature
        get_attribute('temperature').to_f
      end
    end
  end
end
module Thermostat
  module Sensors

    # Class to represent a 1 wire network branch controller (DS2405)
    # However, in this case, it is assumed the chip is controlling a relay.
    # This class has a property to determine if the relay is on or off,
    # and includes methods for switching the relay on or off
    class RelaySensor < Sensors::Base

      # Whether the relay is currently on
      def on?
        get_attribute('PIO').to_i == 1
      end

      # Ensures the relay is off
      def turn_off
        if on?
          set_attribute('PIO', 0)
        end
      end

      # Ensures the relay is on
      def turn_on
        unless on?
          set_attribute('PIO', 1)
        end
      end
    end
  end
end
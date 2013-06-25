module Thermostat
  module States
    class Cooling < States::Base

      def name
        'Cooling'
      end

      def entry
        @io.activate_cooler
      end

      def update_state
        temp = @io.get_temperature_status

        if (temp == ThermostatIO::TEMP_LOW || temp == ThermostatIO::TEMP_GOOD_LOW) && @io.cooler_switch_delay_passed?
          Idle.new(@io)
        else
          self
        end
      end

      def exit
        @io.deactivate_cooler
      end
    end
  end
end
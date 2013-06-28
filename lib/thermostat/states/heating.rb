module Thermostat
  module States
    class Heating < States::Base

      def name
        'Heating'
      end

      def entry
        @io.activate_heater
      end

      def update_state
        temp = @io.get_temperature_status

        if (temp == ThermostatIO::TEMP_HIGH || temp == ThermostatIO::TEMP_GOOD_HIGH) && @io.heater_switch_delay_passed?
          Idle.new(@io)
        else
          self
        end
      end

      def exit
        @io.deactivate_heater
      end
    end
  end
end
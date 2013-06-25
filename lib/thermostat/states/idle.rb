module Thermostat
  module States
    class Idle < States::Base

      def name
        'Idle'
      end

      def entry
      end

      def update_state
        temp = @io.get_temperature_status

        if temp == ThermostatIO::TEMP_HIGH && @io.cooler_switch_delay_passed?
          Cooling.new(@io)
        else
          self
        end
      end

      def exit
      end
    end
  end
end
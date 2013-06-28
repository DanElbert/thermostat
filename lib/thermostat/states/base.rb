module Thermostat
  module States
    class Base

      attr_reader :io

      def initialize(io)
        @io = io
      end

      def entry
        raise "Override me"
      end

      def update_state
        raise "Override me"
      end

      def exit
        raise "Override me"
      end

      def name
        "Base; something's broken"
      end
    end
  end
end
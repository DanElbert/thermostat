module Thermostat
  module Sensors
    # Base class for accessing a single 1 wire device
    class Base
      def initialize(owfs_path_info, sensor_id)
        # ensure the sensor is of the correct form
        sensor_id = sensor_id.strip
        raise "(#{sensor_id}) is not a valid sensor of the form XX.XXXXXXXXXXXX" unless /^\d{2}\.[0-9a-fA-F]{12}$/.match(sensor_id)

        @path_info = owfs_path_info
        @sensor_id = sensor_id
      end

      def id
        get_attribute('id')
      end

      def address
        get_attribute('address')
      end

      protected

      def get_attribute(name)
        File.read(@path_info.get_attribute_path(@sensor_id, name))
      end

      def set_attribute(name, value)
        File.write(@path_info.get_attribute_path(@sensor_id, name), value)
      end
    end
  end
end
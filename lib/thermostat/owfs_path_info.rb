module Thermostat
  class OwfsPathInfo

    attr_accessor :use_cache

    def initialize(owfs_path, use_cache = false)
      @base_path = Pathname.new(owfs_path.to_s)
      @use_cache = use_cache

      raise "owfs path [#{owfs_path}] should be a valid directory" unless @base_path.directory?
      raise "owfs path doesn't appear to be a valid owfs mount point" unless @base_path.join('uncached').directory? && @base_path.join('bus.0').directory?
    end

    def get_sensor_path(sensor_id)
      get_sensor_pathname(sensor_id).to_s
    end

    def get_attribute_path(sensor_id, attribute)
      get_attribute_pathname(sensor_id, attribute).to_s
    end

    private

    def get_sensor_pathname(sensor_id)
      if @use_cache
        path = @base_path.join(sensor_id)
      else
        path = @base_path.join('uncached', sensor_id)
      end

      raise "Invalid Sensor id: #{sensor_id} in \"#{@base_path}\"" unless path.directory?
      path
    end

    def get_attribute_pathname(sensor_id, attribute)
      path = get_sensor_pathname(sensor_id).join(attribute)
      raise "Invalid Sensor Attribute [#{attribute}] for sensor [#{sensor_id}]" unless path.file?
      path
    end
  end
end
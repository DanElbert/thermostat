module Thermostat
  class Config

    CONFIG_ATTRIBUTES = [
        :owfs_mount,
        :air_temperature_id,
        :cooler_relay_id,
        :heater_relay_id,
        :target_temp,
        :switch_delay,
        :max_temperature_delta,
        :state_manager_delay
    ]

    CONFIG_ATTRIBUTES.each { |a| attr_accessor a }

    def self.load_from_file(file)
      config = self.new()
      config.update(file)
    end

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

    def update(file = nil)

      file = @last_loaded_from unless file

      yml = YAML.load_file(file)

      CONFIG_ATTRIBUTES.map { |a| a.to_s }.each do |a|
        if yml.has_key? a
          self.send("#{a}=", yml[a])
        end
      end

      @last_loaded_from = file

      self
    end

    def save(file)
      yml = {}

      CONFIG_ATTRIBUTES.each do |a|
        yml[a] = self.send(a);
      end

      File.open(file, 'w') do |f|
        f.write(YAML.dump(yml))
      end

      self
    end
  end
end
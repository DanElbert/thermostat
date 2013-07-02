module Thermostat
  class Config

    CONFIG_ATTRIBUTES = [
        {name: :owfs_mount, type: :string },
        {name: :air_temperature_id, type: :string },
        {name: :cooler_relay_id, type: :string },
        {name: :heater_relay_id, type: :string },
        {name: :target_temp, type: :float },
        {name: :switch_delay, type: :integer },
        {name: :max_temperature_delta, type: :float },
        {name: :state_manager_delay, type: :integer }
    ]

    CONFIG_ATTRIBUTES.each do |a|
      attr_reader a[:name]

      define_method "#{a[:name]}=".to_sym do |value|
        value = value.to_f if a[:type] == :float
        value = value.to_i if a[:type] == :integer
        instance_variable_set("@#{a[:name]}", value)
      end
    end

    def self.load_from_file(file)
      config = self.new()
      config.update(file)
    end

    def self.load_default
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

      CONFIG_ATTRIBUTES.map { |a| a[:name].to_s }.each do |a|
        if yml.has_key? a
          self.send("#{a}=", yml[a])
        end
      end

      @last_loaded_from = file

      self
    end

    def save(file = nil)
      file = @last_loaded_from unless file

      yml = {}

      CONFIG_ATTRIBUTES.each do |a|
        yml[a[:name].to_s] = self.send(a[:name])
      end

      File.open(file, 'w') do |f|
        f.write(YAML.dump(yml))
      end

      self
    end
  end
end
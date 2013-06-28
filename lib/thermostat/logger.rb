module Thermostat
  class Logger
    def log(state)
      time = Time.new().strftime("%Y-%m-%d %H:%M:%S")
      puts "#{time} -- State: #{state.name}  Temp: #{state.io.get_air_temperature}  Cooler: #{state.io.cooler_on?}  Heater: #{state.io.heater_on?}"

      io = state.io
      config = io.config

      entry = LogEntry.new
      entry.timestamp = Time.new
      entry.state = state.name
      entry.temperature = io.get_air_temperature
      entry.target_temperature = config.target_temp
      entry.max_delta = config.max_temperature_delta
      entry.switch_delay = config.switch_delay
      entry.is_heating = io.heater_on?
      entry.is_cooling = io.cooler_on?

      entry.save!
    end
  end
end
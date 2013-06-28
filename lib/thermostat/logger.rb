module Thermostat
  class Logger
    def log(state)
      time = Time.new().strftime("%Y-%m-%d %H:%M:%S")
      puts "#{time} -- State: #{state.name}  Temp: #{state.io.get_air_temperature}  Cooler: #{state.io.cooler_on?}  Heater: #{state.io.heater_on?}"
    end
  end
end
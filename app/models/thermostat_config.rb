class ThermostatConfig
  include ActiveModel::Validations

  attr_accessor :target_temp, :switch_delay, :max_temperature_delta, :state_manager_delay

  validates :target_temp, :switch_delay, :max_temperature_delta, :state_manager_delay, presence: true
  validates :target_temp, :max_temperature_delta, numericality: true
  validates :state_manager_delay, :switch_delay, numericality: { only_integer: true }

  validates :switch_delay, range: { min: 15 }
  validates :state_manager_delay, range: { min: 5, max: 300 }

  def initialize(attrs = {})
    @real_config = Thermostat::Config.load_from_file(THERMOSTAT_CONFIG)

    self.target_temp = attrs[:target_temp] || @real_config.target_temp
    self.switch_delay = attrs[:switch_delay] || @real_config.switch_delay
    self.max_temperature_delta = attrs[:max_temperature_delta] || @real_config.max_temperature_delta
    self.state_manager_delay = attrs[:state_manager_delay] || @real_config.state_manager_delay
  end

  def save
    if valid?
      @real_config.target_temp = target_temp
      @real_config.switch_delay = switch_delay
      @real_config.max_temperature_delta = max_temperature_delta
      @real_config.state_manager_delay = state_manager_delay
      @real_config.update()
      true
    else
      false
    end
  end

end
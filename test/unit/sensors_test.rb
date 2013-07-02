require File.expand_path('../../test_helper', __FILE__)

class SensorTest < ActiveSupport::TestCase
  def setup
    create_fake_owfs_mount
    setup_path_info_and_config
  end

  def test_temperature_sensor
    @owfs_path.use_cache = false
    sensor = Thermostat::Sensors::TemperatureSensor.new(@owfs_path, @config.air_temperature_id)

    assert_equal @config.air_temperature_id + "FF", sensor.address
    assert_equal @config.air_temperature_id, sensor.id
    assert_equal 26.1, sensor.temperature

    @owfs_path.use_cache = true
    sensor = Thermostat::Sensors::TemperatureSensor.new(@owfs_path, @config.air_temperature_id)
    assert_equal @config.air_temperature_id + "CC", sensor.address
  end

  def test_relay_sensor
    @owfs_path.use_cache = false
    sensor = Thermostat::Sensors::RelaySensor.new(@owfs_path, @config.cooler_relay_id)

    assert_equal @config.cooler_relay_id + "FF", sensor.address
    assert_equal @config.cooler_relay_id, sensor.id
    refute sensor.on?

    sensor.turn_on
    assert sensor.on?

    sensor.turn_off
    refute sensor.on?

    @owfs_path.use_cache = true
    sensor = Thermostat::Sensors::TemperatureSensor.new(@owfs_path, @config.cooler_relay_id)
    assert_equal @config.cooler_relay_id + "CC", sensor.address
  end

end
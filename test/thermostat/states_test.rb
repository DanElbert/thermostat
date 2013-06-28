require File.expand_path('../test_helper', __FILE__)

class StatesTest < MiniTest::Unit::TestCase
  def setup
    create_fake_owfs_mount
    setup_path_info_and_config
    @io = Thermostat::ThermostatIO.new(@config)
  end

  def test_idle_to_cool
    set_attribute(@config.air_temperature_id, 'temperature', 100)
    set_attribute(@config.cooler_relay_id, 'PIO', 0)

    state = Thermostat::States::Idle.new(@io)
    state.entry()
    assert_equal state, state.update_state

    # raise temp over threshold
    set_attribute(@config.air_temperature_id, 'temperature', 120)
    new_state = state.update_state
    state.exit()
    new_state.entry()

    assert_equal "Cooling", new_state.name
    assert_attribute(@config.cooler_relay_id, 'PIO', 1)
  end

  def test_cool_to_idle_within_cooldown
    set_attribute(@config.air_temperature_id, 'temperature', 120)
    set_attribute(@config.cooler_relay_id, 'PIO', 0)

    # Start with the cooler running
    state = Thermostat::States::Cooling.new(@io)
    state.entry()
    assert_equal state, state.update_state

    assert_attribute(@config.cooler_relay_id, 'PIO', 1)

    # Now drop the temp
    set_attribute(@config.air_temperature_id, 'temperature', 80)
    # The first call to update_state should return cooling yet
    assert_equal state, state.update_state

    sleep 1

    # now, the cooler should return to Idle
    new_state = state.update_state
    state.exit()
    new_state.entry()

    assert_equal "Idle", new_state.name
    assert_attribute(@config.cooler_relay_id, 'PIO', 0)
  end
end
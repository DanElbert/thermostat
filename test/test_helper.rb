ENV["RAILS_ENV"] ||= "test"
require File.expand_path('../../config/environment', __FILE__)
require 'rails/test_help'
require "minitest/reporters"

MiniTest::Reporters.use!

# Hacky hack to redefine this constant... maybe it shouldn't be a constant...
self.class.send(:remove_const, :THERMOSTAT_CONFIG)
THERMOSTAT_CONFIG = Rails.root.join('tmp', 'test_thermostat_config.yml')
ONE_WIRE_MOUNT = Rails.root.join('tmp', 'fakeOwfsMount')

class ActiveSupport::TestCase
  ActiveRecord::Migration.check_pending!
  fixtures :all

  def reset_thermostat_config_file
    config = Thermostat::Config.load_default
    config.owfs_mount = ONE_WIRE_MOUNT
    config.air_temperature_id = '01.1234567890AB'
    config.cooler_relay_id = '03.34567890AB12'
    config.heater_relay_id = '04.4567890AB123'

    config.target_temp = 100
    config.switch_delay = 0.25
    config.max_temperature_delta = 5
    config.save(THERMOSTAT_CONFIG)
    config
  end

  def set_attribute(sensor_id, attribute, value, update_cache = true)
    File.write(File.join(ONE_WIRE_MOUNT, 'uncached', sensor_id, attribute), value)
    File.write(File.join(ONE_WIRE_MOUNT, sensor_id, attribute), value) if update_cache
  end

  def assert_attribute(sensor_id, attribute, value, check_cache = false)
    if check_cache
      file = File.join(ONE_WIRE_MOUNT, sensor_id, attribute)
    else
      file = File.join(ONE_WIRE_MOUNT, 'uncached', sensor_id, attribute)
    end

    assert_equal value.to_s, File.read(file).strip
  end

  def setup_path_info_and_config
    @config = reset_thermostat_config_file
    @owfs_path = Thermostat::OwfsPathInfo.new(@config.owfs_mount)
  end

  def create_fake_owfs_mount
    clear_fake_owfs_mount

    devices = [
        {id: '01.1234567890AB', attributes: { temperature: 26.1 } },
        {id: '02.234567890AB1', attributes: { temperature: 5.5 } },
        {id: '03.34567890AB12', attributes: { PIO: 0 } },
        {id: '04.4567890AB123', attributes: { PIO: 0 } }
    ]

    mount_root = ONE_WIRE_MOUNT
    Dir.mkdir(mount_root)
    Dir.mkdir(File.join(mount_root, 'uncached'))
    Dir.mkdir(File.join(mount_root, 'bus.0'))

    devices.each do |d|
      Dir.mkdir(File.join(mount_root, 'uncached', d[:id]))
      Dir.mkdir(File.join(mount_root, d[:id]))

      attrs = { id: d[:id] }.merge(d[:attributes])

      attrs.each do |k, v|
        File.write(File.join(mount_root, 'uncached', d[:id], k.to_s), v)
        File.write(File.join(mount_root, d[:id], k.to_s), v)
      end

      File.write(File.join(mount_root, 'uncached', d[:id], 'address'), d[:id] + "FF")
      File.write(File.join(mount_root, d[:id], 'address'), d[:id] + "CC")
    end

  end

  def clear_fake_owfs_mount
    mount_root = ONE_WIRE_MOUNT
    FileUtils.rm_r(mount_root) if Dir.exists? mount_root
  end
end

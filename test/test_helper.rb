require File.expand_path('../../lib/thermostat', __FILE__)
require 'fileutils'
require 'minitest/autorun'

class MiniTest::Unit::TestCase

  def owfs_mount
    File.expand_path('../fakeOwfsMount/', __FILE__)
  end

  def set_attribute(sensor_id, attribute, value, update_cache = true)
    File.write(File.join(owfs_mount, 'uncached', sensor_id, attribute), value)
    File.write(File.join(owfs_mount, sensor_id, attribute), value) if update_cache
  end

  def assert_attribute(sensor_id, attribute, value, check_cache = false)
    if check_cache
      file = File.join(owfs_mount, sensor_id, attribute)
    else
      file = File.join(owfs_mount, 'uncached', sensor_id, attribute)
    end

    assert_equal value.to_s, File.read(file).strip
  end

  def setup_path_info_and_config
    @config = Thermostat::Config.load
    @config.owfs_mount = owfs_mount
    @config.air_temperature_id = '01.1234567890AB'
    @config.cooler_relay_id = '03.34567890AB12'

    @config.target_temp = 100
    @config.switch_delay = 0.25
    @config.max_temperature_delta = 5

    @owfs_path = Thermostat::OwfsPathInfo.new(@config.owfs_mount)
  end

  def create_fake_owfs_mount
    clear_fake_owfs_mount

    devices = [
        {id: '01.1234567890AB', attributes: { temperature: 26.1 } },
        {id: '02.234567890AB1', attributes: { temperature: 5.5 } },
        {id: '03.34567890AB12', attributes: { PIO: 1 } },
        {id: '04.4567890AB123', attributes: { PIO: 0 } }
    ]

    mount_root = owfs_mount
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
    mount_root = owfs_mount
    FileUtils.rm_r(mount_root) if Dir.exists? mount_root
  end
end
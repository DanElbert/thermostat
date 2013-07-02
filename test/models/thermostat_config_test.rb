require File.expand_path('../../test_helper', __FILE__)

class LogEntryTest < ActiveSupport::TestCase

  test "load from file" do
    c = reset_thermostat_config_file
  end

end

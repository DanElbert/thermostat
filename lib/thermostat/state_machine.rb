module Thermostat
  class StateMachine

    def initialize(starting_state, config)
      @config = config
      @logger = Thermostat::Logger.new
      starting_state.entry
      set_state(starting_state)
    end

    def run
      while true
        @config.update()
        set_state(@current_state.update_state)
        sleep @config.state_manager_delay
      end
    end

    private

    def set_state(new_state)
      if @current_state && @current_state != new_state
        @current_state.exit
        new_state.entry
      end

      @logger.log(new_state)
      @current_state = new_state
    end
  end
end
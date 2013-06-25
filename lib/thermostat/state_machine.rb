module Thermostat
  class StateMachine

    def initialize(starting_state, loop_delay)
      @loop_delay = loop_delay
      starting_state.entry
      set_state(starting_state)
    end

    def run
      while true
        set_state(@current_state.update_state)
        sleep @loop_delay
      end
    end

    private

    def set_state(new_state)
      if @current_state && @current_state != new_state
        @current_state.exit
        new_state.entry
      end

      @current_state = new_state
    end
  end
end
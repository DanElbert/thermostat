class LogController < ApplicationController

  def index
    @entries = LogEntry.order('`timestamp` DESC').limit(100)
  end

  def log_entries
    @entries = LogEntry.order('`timestamp` DESC').limit(100)

    render :json => @entries.to_a.reverse.to_json
  end

end
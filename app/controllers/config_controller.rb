class ConfigController < ApplicationController
  def edit
    @config = ThermostatConfig.new
  end

  def update

    @config = ThermostatConfig.new(params[:config])
    if @config.save
      redirect_to root_path, notice: 'Configuration Updated'
    else
      render :edit
    end
  end
end

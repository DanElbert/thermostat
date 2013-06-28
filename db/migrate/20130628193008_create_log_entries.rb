class CreateLogEntries < ActiveRecord::Migration
  def change
    create_table :log_entries do |t|
      t.datetime :timestamp
      t.string :state
      t.float :temperature
      t.float :target_temperature
      t.float :max_delta
      t.integer :switch_delay
      t.boolean :is_heating
      t.boolean :is_cooling
    end
  end
end

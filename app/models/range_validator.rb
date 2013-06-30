class RangeValidator < ActiveModel::EachValidator
  def validate_each(record, attribute, value)
    return unless value

    if options[:min] && value < options[:min]
      record.errors[attribute] << (options[:message] || "is too low")
    end

    if options[:max] && value > options[:max]
      record.errors[attribute] << (options[:message] || "is too high")
    end
  end

  def check_validity!
    raise ArgumentError, "a min or max must be specified" unless options[:min] || options[:max]
  end
end
require 'rake/testtask'

desc "Run all the tests"
task :default => [:test]

Rake::TestTask.new do |i|
  i.test_files = FileList['test/*_test.rb']
  i.verbose = false
end
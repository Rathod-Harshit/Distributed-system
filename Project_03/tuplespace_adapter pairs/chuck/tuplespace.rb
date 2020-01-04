#!/usr/bin/env ruby
#   Assignment : CPSC-551 Project_03
#   Author     : From Project_02
#   MOdified by: Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#                Rahul Chauhan        (rahulchauhan@csu.fullerton.edu)
#   Program    : it is modified to use zmq instead of udp.


require 'json'
require 'rinda/tuplespace'

require './config'
require './multiplenotify'
require './zpub'

def start_tuplespace(name, uri)
  ts = Rinda::TupleSpace.new
  DRb.start_service(uri, ts)
  puts "Tuplespace #{name} started at #{DRb.uri}"
  ts
end

def map_symbols_out(tuple)
  tuple.map do |item|
    (item.is_a? Symbol)? { :symbol => item } : item
  end
end

config = read_config

ts_name = config['name']
ts_uri  = config['uri']

notify_addrs = config['notify']

ts = start_tuplespace ts_name, ts_uri

begin
  publish = connect_xsub
  puts "Publishing notifications to tcp://#{notify_addrs[0]['address']}:#{notify_addrs[0]['port']}"
  zmq_push publish, "#{ts_name} start 0 #{ts_uri}"

  mn = MultipleNotify.new ts, nil, config['filters']
  loop do
    event, tuple = mn.pop
  json = JSON.generate(map_symbols_out(tuple))
  puts "#{ts_name} #{event} #{json}"
  end

  DRb.thread.join
rescue Interrupt
  puts
ensure
  publish.close
  DRb.stop_service
end

#!/usr/bin/env ruby
#   Assignment : CPSC-551 Project_03
#   Author     : From Project_02
#   MOdified by: Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#                Rahul Chauhan        (rahulchauhan@csu.fullerton.edu)
#   Program    : adapter is modified to get the order of events from clients
#                and use it to determine if the message is in order.
#                If not it asks the ts_managers to give it those messages.


require 'rinda/rinda'
require 'xmlrpc/server'
require 'json'

require './config'
require './zpub'
require './suppress_warnings'

suppress_warnings do
    XMLRPC::Config::ENABLE_NIL_PARSER = true
    XMLRPC::Config::ENABLE_NIL_CREATE = true
end

def start_tuplespace_proxy(name, uri)
  DRb.start_service
  rinda = DRbObject.new_with_uri uri
  Rinda::TupleSpaceProxy.new rinda
end

def map_templates_in(tuple)
  (map_symbols_in tuple).map do |item|
    unless item.is_a? Hash
      item
    else
      if item.key? 'class'
        Module.const_get item['class']
      elsif item.key? 'regexp'
        Regexp.new item['regexp']
      elsif item.key? 'from' and item.key? 'to'
        Range.new item['from'], item['to']
      else
        raise ArgumentError.new "Unexpected tuple item: #{item.inspect}"
       end
    end
  end
end

def map_symbols_in(tuple)
  tuple.map do |item|
    if item.is_a? Hash and item.key? 'symbol'
      item['symbol'].to_sym
    else
      item
    end
  end
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

adapter_host        = config['adapter']['host']
adapter_port        = config['adapter']['port']
adapter_max_clients = config['adapter']['max_clients']

adapter_uri = "http://#{adapter_host}:#{adapter_port}"

ts = start_tuplespace_proxy ts_name, ts_uri

server = XMLRPC::Server.new(adapter_port, adapter_host, adapter_max_clients)
puts "Adapter for tuplespace #{ts_name} started at #{adapter_uri}"


begin
  publish = connect_xsub
  puts "Publishing notifications to tcp://#{notify_addrs[0]['address']}:#{notify_addrs[0]['port']}"
  zmq_push publish, "#{ts_name} adapter 0 #{adapter_uri}"
ensure
  publish.close
end

last_msg = 0

server.add_handler('_in') do |tuple, event_no, sec|
  begin
    if event_no > last_msg
      # do not create a deadlock publish it to queue
      publish = connect_xsub
      json = JSON.generate(map_symbols_out(tuple))
      zmq_push publish, "#{ts_name} take #{event_no} #{json}"
      publish.close      
      if event_no == last_msg + 1
        last_msg = event_no
        map_symbols_out(ts.take map_templates_in(tuple), sec)
      else
        puts "ask for updates"
        publish = connect_xsub
        zmq_push publish, "#{ts_name} lag #{last_msg} #{event_no}"
        publish.close
      end
    end
  rescue Rinda::RequestExpiredError
    nil
  end
end

server.add_handler('_rd') do |tuple, event_no, sec|
  begin
    map_symbols_out(ts.read map_templates_in(tuple), sec)
  rescue Rinda::RequestExpiredError
    nil
  end
end

server.add_handler('_out') do |tuple, event_no|
  if event_no > last_msg
    publish = connect_xsub
    json = JSON.generate(map_symbols_out(tuple))
    zmq_push publish, "#{ts_name} write #{event_no} #{json}"
    publish.close
    if event_no == last_msg + 1
      last_msg = event_no
      ts.write map_symbols_in(tuple)
      nil
    else
      puts "ask for updates"
      publish = connect_xsub
      zmq_push publish, "#{ts_name} lag #{last_msg} #{event_no}"
      publish.close
    end
  end
end

server.add_handler('_reset') do |event_no|
    last_msg = event_no
    nil
end

server.add_handler('_ready') do |lm_clock|
  puts lm_clock
  nil
end

server.serve

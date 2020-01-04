require 'rubygems'
require 'ffi-rzmq'

def connect_xsub
  context = ZMQ::Context.new(1)
  publish = context.socket(ZMQ::PUB)
  publish.connect("tcp://127.0.0.1:5560")
  publish
end

def zmq_push(publish, notification)
  sleep 1
  publish.send_string notification
  puts notification
end
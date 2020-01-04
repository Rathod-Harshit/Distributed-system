#!/usr/bin/env python3

#
#   Assignment : CPSC-551 Project_03
#   Authors    : Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#                Rahul Chauhan        (rahulchauhan@csu.fullerton.edu)
#   Program    : Interactive client. Orders events using lamport clock, which
#                is shared by other clients. Also check if adapter is up,
#                if not it retries twice(2*99s) and then exits.

import code
import zmq
import time
import proxy
   
local_clock = 0
ts = proxy.TupleSpaceAdapter('http://localhost:8001')

def check_if_ready():
    try:
        ts._ready(local_clock)
        return("ok")
    except:
        print("Adapter not ready")

def wait():
    for i in reversed(range(1,99)):
        print(f"Retrying in {i}s...")
        time.sleep(1)
    final = check_if_ready()
    if final != "ok":
        print("Service can`t be invoked now. Please try later.")
    else:
        return("ok")

def connect():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")
    socket.send_pyobj(local_clock)
    message = socket.recv_pyobj()
    return message

def write(ms):
    chk= check_if_ready()
    if chk != "ok":
        chk = wait()
        if chk != "ok":
            exit()
    event_counter = connect()
    global local_clock
    local_clock = event_counter
    ts._out(ms, event_counter)

    
def take(ms):
    chk= check_if_ready()
    if chk != "ok":
        chk = wait()
        if chk != "ok":
            exit()
    event_counter = connect()
    global local_clock
    local_clock = event_counter
    print(ts._in(ms, event_counter))

def read(ms):
    chk= check_if_ready()
    if chk != "ok":
        chk = wait()
        if chk != "ok":
            exit()
    print(ts._rd(ms, 0))

if __name__ == "__main__":
    chk = check_if_ready()
    if chk != "ok":
        chk = wait()
        if chk != "ok":
            exit()

code.interact(local=locals())

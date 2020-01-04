#
#   Assignment : CPSC-551 Project_03
#   Authors    : Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#   Program    : Lamport clock for all the clients. Clients send their own 
#                timestamps and get the global clock in return. It helps in
#                ordering of events. 

import time
import zmq


def event(message, lamport_clock):

    lamport_clock = max(lamport_clock, message) + 1
    return lamport_clock        


context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")
lamport_clock = 0

while True:
    #  Wait for next request from client
    message = socket.recv_pyobj()

    #  Do some 'work'
    time.sleep(1)
    print("Received request: %s" % message)

    count = event(message, lamport_clock)
    lamport_clock = count
    #  Send reply back to client
    socket.send_pyobj(count)






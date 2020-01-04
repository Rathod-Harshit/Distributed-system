#
#   Assignment : CPSC-551 Project_03
#   Authors    : Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#   Program    : Tuplespace manager. Listen to all events and logs them. 
#                Uses XPUB/XSUB.
#                 

import time
import zmq
import logrec
import proxy

# Subscriber connect to XPUB - tsm
context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://127.0.0.1:5559")
subscriber.setsockopt_string(zmq.SUBSCRIBE, '')
tsm = "Alice"
print(f"{tsm} Subscribed to tcp://127.0.0.1:5559")

local_count = 0
events = ["write", "take"]

while True:
    data = subscriber.recv()
    notification = data.decode()
    print("Received request: %s" % notification)
    notification = notification.split(' ', 3)

    if notification[1] in events:
        local_count = local_count + 1
        # Remove duplicates
        if int(notification[2]) >= local_count:
            # Log all the write and take events
            ada_chk = logrec.create_att(tsm,notification[1],notification[2],notification[3])
            if notification[0] != tsm:
                # if the event is from other ts then write it
                ts = proxy.TupleSpaceAdapter('http://localhost:8000')
                tup_le = json.loads(notification[3])
                try:
                    if notification[1] == "write":
                        ts._out(tup_le, notification[2])
                    if notification[1] == "take":
                        ts._in(tup_le, notification[2])
                except:
                    print("Adapter address http://localhost:8000 not active")

#   order 0 means it is either start of ts or adapter
    if (notification[0] == tsm and notification[2] == "0"):
        #print("log it, chk for restart")
        logrec.create_att(notification[0],notification[1],local_count,notification[3])

#   lag command is issued when ts is missing some updates.        
    if (notification[0] == tsm and notification[1] == "lag"):
        logrec.create_att(notification[0],notification[1],notification[2],notification[3])
        

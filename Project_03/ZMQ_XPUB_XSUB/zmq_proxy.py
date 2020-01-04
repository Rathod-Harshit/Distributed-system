#
#   Assignment : CPSC-551 Project_03
#   Authors    : Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#   Program    : ZMQ_PROXY. It allows many to many pub sub model. No need 
#                to use multiple ports. Publishers can publish to one port
#                and subscribers can subscribe to a single port

import zmq

def main():
    """ main method """

    context = zmq.Context()
    print("Binding tcp://*:5559 with tcp://*:5560")
    # Socket facing clients
    frontend = context.socket(zmq.XPUB)
    frontend.bind("tcp://*:5559")

    # Socket facing services
    backend  = context.socket(zmq.XSUB)
    backend.bind("tcp://*:5560")

    zmq.proxy(frontend, backend)

    # We never get here…
    frontend.close()
    backend.close()
    context.term()

if __name__ == "__main__":
    main()

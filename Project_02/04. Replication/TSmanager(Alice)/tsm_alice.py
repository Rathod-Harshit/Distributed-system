#!/usr/bin/env python3

#   Assignment : CPSC-551 Project_02
#   Authors    : Rahul Chauhan        (rahulchauhan@csu.fullerton.edu)
#                Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#   Program    : Tsmanager for tuplespace

import sys
import struct
import socket
import logrec
import proxy
import json

# per <https://en.wikipedia.org/wiki/User_Datagram_Protocol>
MAX_UDP_PAYLOAD = 65507


def main(address, port):
    # See <https://pymotw.com/3/socket/multicast.html> for details

    server_address = ('', int(port))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)

    group = socket.inet_aton(address)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    print(f"Listening on udp://{address}:{port}")
    tsm_name = "Alice"
    print(f"TSmanager started for {tsm_name}")

    try:
        while True:
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            notification = notification.split(' ', 2)
            sys.argv[1:] = []
            # Create a log for the events and recover if required
            if (notification[0] == tsm_name or notification[1] == "write" or notification[1] == "take"):
                ada_chk = logrec.create_att(tsm_name, notification[1], notification[2])
            # write events of others to own tuplespace and block replication of own messages 
            if (notification[0] != tsm_name and (notification[1] == "write" or notification[1] == "take")):
                if ada_chk != None:
                    ts = proxy.TupleSpaceAdapter('http://localhost:8000')
                    tup_le = json.loads(notification[2])
                    try:
                        ts._out(tup_le)
                    except:
                        print("Adapter address http://localhost:8000 not active")
    except:
        sock.close()


def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])

    sys.exit(main(*sys.argv[1:]))

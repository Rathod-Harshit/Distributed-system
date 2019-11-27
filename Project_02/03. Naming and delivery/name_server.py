#!/usr/bin/env python3

#   Assignment : CPSC-551 Project_02
#   Authors    : Rahul Chauhan        (rahulchauhan@csu.fullerton.edu)
#                Harshit Singh Rathod (rathod10892@csu.fullerton.edu)
#   Program    : Naming server

import sys
import struct
import socket
import proxy


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


    try:
        while True:
            data, _ = sock.recvfrom(MAX_UDP_PAYLOAD)
            notification = data.decode()
            notification = notification.split(' ', 2)
            # if event is adapter then connect to naming tuplespace and try getting the list of users
            if notification[1] == "adapter":
                ts = proxy.TupleSpaceAdapter('http://localhost:8004')
                try:
                    users = ts._inp(["users", None])[1]
                except:
                    users = []
            # if user already exists then take the adapter_uri from tuple else add the user
                if notification[0] in users:
                    ts._in([notification[0], None])
                else:
                    users.append(notification[0])
            # finally write the new user list and (name,adapter_uri) pair
                ts._out(["users", users])
                ts._out([notification[0], notification[2]])
    except:
        sock.close()


def usage(program):
    print(f'Usage: {program} ADDRESS PORT', file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        usage(sys.argv[0])

    sys.exit(main(*sys.argv[1:]))

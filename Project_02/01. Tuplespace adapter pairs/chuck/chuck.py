#!/usr/bin/env python3

import proxy

ts = proxy.TupleSpaceAdapter('http://localhost:8002')

ts._out(["chuck", "distsys", "I like systems more than graphs"])



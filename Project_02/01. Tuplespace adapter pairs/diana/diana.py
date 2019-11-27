#!/usr/bin/env python3

import proxy

ts = proxy.TupleSpaceAdapter('http://localhost:8003')

ts._out(["diana", "distsys", "I like systems more than graphs"])



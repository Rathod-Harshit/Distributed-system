#!/usr/bin/env python3

import proxy

ts = proxy.TupleSpaceAdapter('http://localhost:8000')

ts._out(["alice", "distsys", "I like systems more than graphs"])
ts._out(["alice", "distsys2", "I like systems more than geo"])
ts._out(["alice", "distsys3", "I like systems more than math"])

ts._in(["alice", "distsys", None])



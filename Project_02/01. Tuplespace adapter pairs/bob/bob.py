import proxy

ts = proxy.TupleSpaceAdapter('http://localhost:8001')

ts._out(["bob", "distsys", "I like systems more than graphs"])
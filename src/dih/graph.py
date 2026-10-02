class Node:
    _count = 1

    def __init__(self, op, name, nice, minargs, maxargs, req_kwargs, line_num):
        self.instance_num = Node._count
        Node._count += 1

        self.op = op
        self.name = name if name is not None else ""
        self.nice = int(nice) if nice is not None else 0

        self.l_edge = {}
        self.ul_edge = []

        self.minargs = max(op.minargs, int(minargs)) if minargs else op.minargs # covers both empty string and None
        self.maxargs = min(op.maxargs, int(maxargs)) if maxargs else op.maxargs
        self.req_kwargs = op.req_kwargs | set(filter(len, req_kwargs.split(","))) if req_kwargs is not None else op.req_kwargs

        self.l_args = {}
        self.ul_args = []
        
        self.line_num = line_num

    def __repr__(self): # for my use!!!
        return str(vars(self))

class Graph:
    def __init__(self):
        self.nodes = {} # instance num to node
        self.registry = {} # name to instance num
        self.active = set()

    def __repr__(self):
        return '\n'.join(repr(self.nodes[nodeid]) for nodeid in self.nodes)

    def add_node(self, node):
        self.nodes[node.instance_num] = node
        if node.name != "":
            if node.name in self.registry:
                raise NameError() # propogated to the parser which has more info
            else:
                self.registry[node.name] = node.instance_num

    def connect(self, node_num1, node_num2, text = None): # missing node is handled by parser
        if text is not None:
            self.nodes[node_num1].l_edge[text] = node_num2
        else:
            self.nodes[node_num1].ul_edge.append(node_num2)

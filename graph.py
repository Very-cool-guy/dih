class Node:
    _count = 1

    def __init__(self, op, name, nice, minargs, maxargs, req_kwargs):
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

    def __repr__(self): # for my use!!!
        return str(self.__dict__)

class Graph:
    def __init__(self):
        self.nodes = {} #instance num to node
        self.registry = {} #name to instance num
        self.active = set()

    def __repr__(self):
        return '\n'.join(self.nodes[nodeid].__repr__() for nodeid in self.nodes)

    def add_node(self, node):
        self.nodes[node.instance_num] = node
        if node.name != "":
            if node.name in self.registry:
                raise ValueError("duplicate")
            else:
                self.registry[node.name] = node.instance_num

    def connect(self, node_num1, node_num2, text = None):
        if node_num1 not in self.nodes or node_num2 not in self.nodes:
            raise NameError("node does not exist")
        else:
            if text is not None:
                self.nodes[node_num1].l_edge[text] = node_num2
            else:
                self.nodes[node_num1].ul_edge.append(node_num2)

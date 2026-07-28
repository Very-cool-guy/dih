class Node:
    _count = 1

    def __init__(self, op, name, nice):
        self.instance_num = Node._count
        Node._count += 1

        self.op = op
        self.name = name if name is not None else ""
        self.nice = nice if nice is not None else 0
        self.l_edge = {}
        self.ul_edge = []
        self.minargs = op.minargs
        self.req_kwargs = op.req_kwargs

    def change_args(self, n_minargs):
        self.minargs = max(n_minargs, self.op.minargs)

    def change_kwargs(self, n_kwargs):
        self.req_kwargs = list(set(self.op.req_kwargs + n_kwargs))

class Graph:
    def __init__(self):
        self.nodes = {} #instance num to node
        self.registry = {} #name to instance num

    def add_node(self, node):
        self.nodes[node.instance_num] = node
        if node.name != "":
            if node.name in self.registry:
                raise ValueError("duplicate")
            else:
                self.registry[node.name] = node.instance_num

    def connect(self, node_num1, node_num2, labeled = False, text = ""):
        if node_num1 not in self.nodes or node_num2 not in self.nodes:
            raise NameError("node does not exist")
        else:
            if labeled:
                self.nodes[node_num1].l_edge[text] = node_num2
            else:
                self.nodes[node_num1].ul_edge.append(node_num2)

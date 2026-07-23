class Operator:
    def __init__(self, minargs):
        self.minargs = minargs # placeholder

class Node:
    _count = 1

    def __init__(self, op, name = "", nice = 0, l_edge = None, ul_edge = None, minargs = -1):
        self.instance_num = Node._count
        Node._count += 1

        self.op = op
        self.name = name
        self.nice = nice
        self.l_edge = l_edge if l_edge is not None else {}
        self.ul_edge = ul_edge if ul_edge is not None else []
        self.minargs = max(minargs, op.minargs)

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

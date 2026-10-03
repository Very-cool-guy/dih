from . import operators

type opstr = str | None

class Node:
    """Model of a dih node, owned by a graph."""
    _count = 1

    def __init__(self, op: operators.Operator, name: opstr, nice: opstr, minargs: opstr, maxargs: opstr, req_kwargs: opstr, line_num: int) -> None:
        self.instance_num = Node._count
        Node._count += 1

        self.op = op
        self.name: str = name if name is not None else ""
        self.nice: int = int(nice) if nice is not None else 0

        self.l_edge: dict[str, int] = {}
        self.ul_edge: list[int] = []

        self.minargs = max(op.minargs, int(minargs)) if minargs else op.minargs # covers both empty string and None
        self.maxargs = min(op.maxargs, int(maxargs)) if maxargs else op.maxargs
        self.req_kwargs: set[str] = op.req_kwargs | set(filter(len, req_kwargs.split(","))) if req_kwargs is not None else op.req_kwargs

        self.l_args = {}
        self.ul_args = []
        
        self.line_num = line_num

    def __repr__(self) -> str: # for my use!!!
        return str(vars(self))

class Graph:
    """Model of a dih graph."""
    def __init__(self) -> None:
        self.nodes: dict[int, Node] = {}
        self.registry: dict[str, int] = {}
        self.active = set()

    def __repr__(self) -> str:
        return '\n'.join(repr(self.nodes[nodeid]) for nodeid in self.nodes)

    def add_node(self, node: Node) -> None:
        """Add a pre-constructed node to the graph."""
        self.nodes[node.instance_num] = node
        if node.name != "":
            if node.name in self.registry:
                raise NameError() # propogated to the parser which has more info
            else:
                self.registry[node.name] = node.instance_num

    def connect(self, node1: int, node2: int, text: str | None = None) -> None: # missing node is handled by parser
        "Connect two nodes in the graph."
        if text is not None:
            self.nodes[node1].l_edge[text] = node2
        else:
            self.nodes[node1].ul_edge.append(node2)

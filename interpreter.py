import sys

def _take(l, n):
    return l if len(l) <= n else l[:n]

def interpret(graph):
    while True:
        lazy_nodes = graph.active.copy()
        added_actives = set()

        for nodeid in sorted(graph.active, key = lambda _id: graph.nodes[_id].nice)[::-1]:
            node = graph.nodes[nodeid]

            if len(node.ul_args) >= node.minargs and set(node.l_args.keys()) >= node.req_kwargs:
                ul_result, l_result = node.op.f(_take(node.ul_args, node.maxargs), node.l_args) 

                if ul_result is not None:
                    for targetid in node.ul_edge:
                        graph.nodes[targetid].ul_args.append(ul_result)

                for text, targetid in node.l_edge:
                    if text in l_result:
                        graph.nodes[targetid].l_args[text] = l_result[text]
                    elif ul_result is not None:
                        graph.nodes[targetid].l_args[text] = ul_result

                lazy_nodes.remove(nodeid) # nodes that do not meet requirements stay
                added_actives.update(node.ul_edge)
                added_actives.update(list(node.l_edge.values()))

                node.ul_args = []
                node.l_args = {}

        if lazy_nodes or added_actives:
            graph.active = lazy_nodes | added_actives
        else:
            sys.exit()

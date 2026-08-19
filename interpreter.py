import ast
import errors

def _take(l, n):
    return l if len(l) <= n else l[:n]

def interpret(graph):
    while graph.active:
        new_actives = set()

        for nodeid in sorted(graph.active, key = lambda _id: graph.nodes[_id].nice)[::-1]:
            node = graph.nodes[nodeid]

            if len(node.ul_args) < node.minargs or not set(node.l_args.keys()) >= node.req_kwargs:
                new_actives.add(nodeid)
                continue
            
            used_args = _take(node.ul_args, node.maxargs)
            try:
                ul_result, l_result = node.op.f(used_args, node.l_args) 
            except Exception as e:
                errors.clean_raise(RuntimeError(f"Operator {node.op.name} on line {node.line_num} failed with args {used_args} and kwargs {node.l_args}"))
                raise e

            match node.op.name:
                case "if": # TODO: should if only accept booleans or not?
                    if ul_result:
                        if "y" in node.l_edge:
                            new_actives.add(node.l_edge["y"])
                    else:
                        if "n" in node.l_edge:
                            new_actives.add(node.l_edge["n"])

                case "case":
                    val_to_id = {ast.literal_eval(text) if text != "else" else "else" : _id for text, _id in node.l_edge.items()}
                    targetid = val_to_id.get(ul_result) or val_to_id.get("else")

                    if targetid is not None:
                        new_actives.add(targetid)
                        graph.nodes[targetid].ul_args.append(ul_result)

                case _:
                    if ul_result is not None:
                        for targetid in node.ul_edge:
                            graph.nodes[targetid].ul_args.append(ul_result)

                    for text, targetid in node.l_edge.items():
                        if text in l_result:
                            graph.nodes[targetid].l_args[text] = l_result[text]
                        elif ul_result is not None:
                            graph.nodes[targetid].l_args[text] = ul_result

                    new_actives.update(node.ul_edge)
                    new_actives.update(list(node.l_edge.values()))

            node.ul_args = []
            node.l_args = {}

        graph.active = new_actives

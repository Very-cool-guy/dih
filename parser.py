import graph, operators

import re

def _add(l, elem, pos):
    if len(l) <= pos:
        l.append(elem)
    else:
        l[pos] = elem

def parse(source):
    result = graph.Graph()

    norm_pattern = re.compile(r'^(?>(\(.+\))?(\[.+\])?(\{\d+\})?)([^/]+)(?:/(\d*),(\d*),(.*))?$')
    arrow_pattern = re.compile(r'^(->|<-)(\(.+\))?(\[.+\])$')

    source = [(len(line) - len(line.lstrip(' ')), line.lstrip(' ')) for line in source.split("\n") if line]
    assert source[0][0] == 0

    last_indents = []
    last_indent_num = -1

    for indent, content in source:
        norm_match = re.search(norm_pattern, content)
        arrow_match = re.search(arrow_pattern, content)
           
        if arrow_match: # arrow match first otherwise will be consumed by .+ in the normal pattern
            if not indent:
                raise SyntaxError("top-level node can not use arrow notation")

            elif indent <= last_indent_num + 1: # this handles both one more indent and less indents
                vals = [arrow_match.group(i) for i in range(1, 4)]
                arrow, in_ledge, node_name = [val[1:-1] if i != 1 and val is not None else val for i, val in enumerate(vals, start=1)] # bad code!!!

                old_id = last_indents[indent - 1]
                new_id = result.registry[node_name]

                if arrow == "->":
                    result.connect(old_id, new_id, text = in_ledge)
                    _add(last_indents, new_id, indent) # not necessarily indented the same as where the node was declared

                elif arrow == "<-":
                    result.connect(new_id, old_id, text = in_ledge)
                    _add(last_indents, old_id, indent) # same node even though indented one more space

            else:
                raise SyntaxError("cannot indent more than one space more than previous line")


        elif norm_match:
            vals = [norm_match.group(i) for i in range(1, 8)]
            in_ledge, node_name, nice, op, minargs, maxargs, req_kwargs = [val[1:-1] if i < 4 and val is not None else val for i, val in enumerate(vals, start=1)]

            if not indent:
                if in_ledge is not None:
                    raise SyntaxError("top-level node can not label arrows pointing towards it")
                new_node = graph.Node(operators.operators[op.strip()], node_name, nice, minargs, maxargs, req_kwargs)
                result.add_node(new_node)
                new_id = new_node.instance_num

                last_indent_num = 0 
                last_indents = [new_id] # pop everything from the last indent registry

            elif indent <= last_indent_num + 1:
                new_node =  graph.Node(operators.operators[op.strip()], node_name, nice, minargs, maxargs, req_kwargs)
                result.add_node(new_node)
                new_id = new_node.instance_num
                last_id = last_indents[indent - 1]
                
                result.connect(last_id, new_id, text = in_ledge)

                last_indent_num = indent
                _add(last_indents, new_id, indent)

            else:
                raise SyntaxError("cannot indent more than one space more than previous line")

        else:
            raise SyntaxError("parsing failure")
        
    return result

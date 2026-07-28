import graph, operators

import re

def parse(source):
    result = graph.Graph()

    norm_pattern = re.compile(r'^(?>(\(.+\))?(\[.+\])?(\{\d+\})?)(.+)$')
    arrow_pattern = re.compile(r'^(->|<-)(\(.+\))?(\[.+\])$')

    source = [(len(line) - len(line.lstrip(' ')), line.lstrip(' ')) for line in source.split("\n") if line]
    assert source[0][0] == 0

    last_nodeid = 0
    last_indents = []
    last_indent_num = -1

    for indent, content in source:
        norm_match = re.search(norm_pattern, content)
        arrow_match = re.search(arrow_pattern, content)

        if norm_match:
            in_ledge, node_name, nice, op = [norm_match.group(i) for i in range(1, 5)]

            if not indent:
                if in_ledge is not None:
                    raise SyntaxError("top-level node can not label arrows pointing towards it")
                new_node = Graph.Node(operators.operators[op.strip()], node_name, nice)
                result.add_node(new_node)

                last_indent_num = 0 
                new_node_id = new_node.instance_num
                last_nodeid = new_node_id
                last_indents = [new_node_id] # pop everything from the last indent registry

            ...

        elif arrow_match:
            if not indent:
                raise SyntaxError("top-level node can not use arrow notation")
            else:
                ...

        else:
            raise SyntaxError("parsing failure")


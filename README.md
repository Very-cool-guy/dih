# the dih programming language
The dih (short for "directed") programming language is probably the first language based on graphs.

## the graph
In dih, a program is a directed graph with labeled and unlabeled edges. You can think of nodes as operators, and edges as passing information between them. Labeled edges basically pipe keyword arguments, while unlabeled ones pipe unnamed arguments.

The graph interpreter starts by activating all nodes that does not have arrows pointed towards them. Each node has conditions they must satisfy to execute. In each clock tick, the operators on these nodes execute in an unreliable order, and pass on the result via edges to other nodes. They then deactivates themselves and activate target nodes. Nodes that do not satisfy their conditions remain active and do not execute until they meet them. If no nodes are activated by the end of a turn, the program terminates.

## the language
The dih language is not so much a programming language as a markup language specifying the graph. Each non-empty line specifies a node. The syntax for a line is:
```
(incoming labeled arrow name)[node name]{niceness}...
```
Each of the bracket groups are optional, and the characters following it specify the operator.

A lot of edges are done implicitly. When a line indents one more space than the previous line, there's an implicit arrow from the node declared previously to the current node. When a line indents less or equal to the previous one, the implicit arrow is from the closest line before with one less indent and a common root node (the *parent* node). It's a common way of specifying a directory tree, for example.

A line can also be an arrow followed by a node name in square brackets. Starting with `->` establishes an arrow from the parent node to the one with the specified name, and the line counts as a declaration for the target node, so if you indent one more space after that line, the implicit arrow starts from the node with the specified name. Dually, starting with `<-` establishes an arrow from the named node to the parent node of the line, and counts as a declaration for the parent, as in you can keep working with the same node.

# basic
- [x] make basic graph and node class
- [x] make basic operator class
- [x] make basic source to graph parser
- [x] make basic graph interpreter
- [x] make main wrapper

YAYYYYYY

# refinement
- [ ] more operators including ones in the library, total library integration is probably impossible since i have to choose argument stuff
- [ ] better errors
- [ ] subgraphs(functions)
- [ ] graph visualisation tool (hard)
- [ ] turn into compiler

# smol
- [x] syntax for changing minargs and req_kwargs
- [ ] lines with standalone names or arrows with names on both sides
- [ ] not possible for literal string to contain / or / to be an operator
- [ ] multiple same name arrows from a node
- [ ] revamp readme im serious!!!
- [ ] type hint (duh)
- [x] (URGENT) change behaviour of unproduced labelled arrow from throwing an error to making giving the produced unlabeled result
- [x] better way to allow empty returns
- [x] if and match
- [ ] match does not accept "else" or undictkeyable values
- [x] make match return a value
- [ ] *? operator family
- [ ] composition of nodes
- [ ] ALSO URGENT `[hi]Lit[7]` matches wrongly, whole thing gets consumed by the bracket group. making it lazy makes bracket group not match anything at all.

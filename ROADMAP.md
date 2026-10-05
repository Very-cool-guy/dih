# Make a working one
- [x] make basic graph and node class
- [x] make basic operator class
- [x] make basic source to graph parser
- [x] make basic graph interpreter
- [x] make main wrapper - YAYYYY!

# v0 release
## Major
- [x] better errors
- [x] overriding minargs and req_kwargs
- [x] type hint (duh)
- [x] if and match
- [x] docstrings
- [ ] conceptualize and (maybe) implement full python interop
- [ ] gui: highlighted editor and graph visualisation on the left. no visual debug/run this release.
## Minor
- [x] not possible for literal string to contain / or / to be an operator
- [x] better way to allow empty returns
- [x] `[hi]Lit[7]` matches wrongly, whole thing gets consumed by the bracket group. making it lazy makes bracket group not match anything at all.
- [x] unproduced labelled arrow gives the unlabeled result instead of throwing
- [x] make match return a value
- [x] gui: fix broken highlighting
- [x] gui: fix the annoying attempted relative import without parent package!!! annoying!!!

# Major; not now
- [ ] subgraphs(functions)
- [ ] messages and triggers
- [ ] composition of nodes; nodes as first-class values
- [ ] oop support
- [ ] make syntax less terrible: non-indentation based, and anything but that suffix notation!
- [ ] continue on the gui

# Minor; not now
- [ ] lines with standalone names or arrows with names on both sides
- [ ] multiple same name arrows from a node
- [ ] revamp readme!!!
- [ ] match does not accept "else" or undictkeyable values
- [ ] *? operator family
- [ ] warnings for failure to override arg reqs
- [ ] the tree-sitter seems to name newlines as nodes? should i care?

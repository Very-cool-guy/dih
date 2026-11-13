from . import Utils

import ast
import functools

from dataclasses import dataclass
from collections.abc import Callable
from types import ModuleType

inf = float('inf')
empty = set()

def adapt(func: Callable) -> Callable:
    def _(args, kwargs):
        return func(*args, **kwargs), {} # only user-defined functions can meaningfully return keyword results.
    return _

@dataclass
class Operator:
    """Model of an operator, which is owned by a graph node."""
    f: Callable
    minargs: int
    maxargs: int | float # you cant type hint float inf apparently.
    req_kwargs: set[str]
    name: str

operators = {
}

def get_op(op_name: str, mod_dict: dict[str, ModuleType], func_dict: dict[str, Callable]) -> Operator:
    """Get an operator by its name."""
    if op_name in ["match", "if"]:
        def _(args, kwargs): # placeholder; implemented specially in the interpreter.
            return args[0], {}
        return Operator(_, 1, 1, empty, op_name)

    if op_name in func_dict:
        return Operator(adapt(func_dict[op_name]), 0, inf, empty, op_name)

    if op_name in operators:
        return operators[op_name]

    for mod in mod_dict.keys():
        if op_name.startswith(mod + "."):
            mod_path = op_name.split(".")
            _ = functools.reduce(getattr, mod_path[1:], mod_dict[mod]) # holy shit that was great to write
            return Operator(adapt(_), 0, inf, empty, op_name)

    try:
        result = ast.literal_eval(op_name) # TODO: think of expressions to ban?
        def _(args, kwargs):
            return result, {}
        return Operator(_, 0, inf, empty, repr(op_name))
    except ValueError:
        raise NameError

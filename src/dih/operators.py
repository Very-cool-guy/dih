from . import Utils

import ast

from dataclasses import dataclass
from collections.abc import Callable

inf = float('inf')
empty = set()

@dataclass
class Operator:
    """Model of an operator, which is owned by a graph node."""
    f: Callable
    minargs: int
    maxargs: int | float # you cant type hint float inf apparently.
    req_kwargs: set[str]
    name: str

class _CoolerDict(dict):
    """Dict wrapper for the operators registry for custom missing behaviour."""
    def __missing__(self, key: str) -> Operator:
        if key.startswith("Lit[") and key.endswith("]"):
            result = ast.literal_eval(key[4:-1])# TODO: think about expressions to disallow
            def f(args, kwargs):
                return result, {}
            return Operator(f, 0, inf, empty, "Literal")
        raise NameError

operators = _CoolerDict({
        "+": Operator(Utils.add, 2, inf, empty, "+"),
        "print": Operator(Utils._print, 1, inf, empty, "print"),
        "input": Operator(Utils._input, 0, inf, empty, "input"),
        "match": Operator(Utils._match, 1, 1, empty, "match"),
        "if": Operator(Utils._if, 1, 1, empty, "if"),
        })

import ast
import Utils

inf = float('inf')
empty = set()

class Operator:
    def __init__(self, f, minargs, maxargs, req_kwargs, special_id = 0): # all are mandatory
        self.f = f
        self.minargs = minargs
        self.maxargs = maxargs
        self.req_kwargs = req_kwargs
        self.special_id = special_id

class _CoolerDict(dict):
    def __missing__(self, key):
        if key.startswith("Lit[") and key.endswith("]"):
            result = ast.literal_eval(key[4:-1])# TODO: think about expressions to disallow
            def f(args, kwargs):
                return result, {}
            return Operator(f, 0, inf, empty)
        
        raise NameError("unrecognized operator")

operators = _CoolerDict({
        "+": Operator(Utils.add, 2, inf, empty),
        "print": Operator(Utils._print, 1, inf, empty),
        "match": Operator(Utils._match, 1, 1, empty, -1),
        "if": Operator(Utils._if, 1, 1, empty, -2),
        })

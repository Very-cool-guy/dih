import ast

inf = float('inf')
empty = set()

def staticclass(cls):
    for name, attr in list(cls.__dict__.items()):
        if callable(attr) and not name.startswith("__"):
            setattr(cls, name, staticmethod(attr))
    return cls

@staticclass
class Utils:
    def add(args, kwargs):
        return sum(args), {}
    def _print(args, kwargs):
        print(*args, **kwargs)
        return None, {}

class Operator:
    def __init__(self, f, minargs, maxargs, req_kwargs): # all are mandatory
        self.f = f
        self.minargs = minargs
        self.maxargs = maxargs
        self.req_kwargs = req_kwargs

class _CoolerDict(dict):
    def __missing__(self, key):
        if key.startswith("Literal[") and key.endswith("]"):
            result = ast.literal_eval(key[8:-1])# TODO: think about expressions to disallow
            def f(args, kwargs):
                return result, {}
            return Operator(f, 0, inf, empty)
        
        raise NameError("unrecognized operator")

operators = _CoolerDict({
        "+": Operator(Utils.add, 2, inf, empty),
        "public.static.void.main.string.args.system.out.println": Operator(Utils._print, 1, inf, empty), # to make our friends at java feel more comfortable
        })

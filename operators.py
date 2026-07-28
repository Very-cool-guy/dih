def staticclass(cls):
    for name, attr in list(cls.__dict__.items()):
        if callable(attr) and not name.startswith("__"):
            setattr(cls, name, staticmethod(attr))
    return cls

@staticclass
class Utils:
    def add(args, kwargs):
        return [sum(args)], kwargs

class Operator:
    def __init__(self, f, minargs, req_kwargs): # all three are mandatory
        self.f = f
        self.minargs = minargs
        self.req_kwargs = req_kwargs

operators = {
        "+": Operator(Utils.add, 2, [])
        }

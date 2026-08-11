__all__ = ["add", "_print", "_match", "_if"]

def add(args, kwargs):
    return sum(args), {}

def _print(args, kwargs):
    print(*args, **kwargs)
    return None, {}

def _match(args, kwargs): # implemented in the interpreter cuz theyre special
    return args[0], {}

def _if(args, kwargs):
    return args[0], {}

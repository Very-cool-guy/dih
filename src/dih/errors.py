BOLD = "\033[1m"
PURPLE = "\033[95m"
RESET = "\033[0m"

def clean_raise(e):
    """Internal helper to format an exception the same way as the python interpreter, without raising the error to cause an ugly stack trace."""
    name = type(e).__name__
    desc = e.args[0]
    print(f"{BOLD}{PURPLE}{name}{RESET}" + f": {PURPLE}{desc}{RESET}")

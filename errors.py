BOLD = "\033[1m"
PURPLE = "\033[95m"
RESET = "\033[0m"

def clean_raise(e):
    name = type(e).__name__
    desc = e.args[0]
    print(f"{BOLD}{PURPLE}{name}{RESET}" + f": {PURPLE}{desc}{RESET}")

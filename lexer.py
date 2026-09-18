def consume(delimiters, string, line = 0):
    if not string.startswith(delimiters[0]):
        return None, string
    end = string.find(delimiters[1])
    if end == -1:
        raise SyntaxError(f"Unclosed {delimiters[0]} on line {line}")
    return string[1:end], string[end+1:]

def lex_normal(string, line):
    in_ledge, string = consume(['(', ')'], string, line)
    node_name, string = consume(['[', ']'], string, line)
    nice, string = consume(['{', '}'], string, line)
    slash = string.rfind("/", 0, string.rfind(",", 0, string.rfind(","))) # last slash before two commas
    if slash == -1:
        op, minargs, maxargs, req_kwargs = string, None, None, None
    else:
        op, string = string[:slash], string[slash+1:]
        items = string.split(',')
        minargs, maxargs, req_kwargs = items[0], items[1], ','.join(items[2:])
    return in_ledge, node_name, nice, op, minargs, maxargs, req_kwargs

def lex_arrow(string):
    try:
        arrow, string = string[:2], string[2:]
        in_ledge, string = consume(['(', ')'], string)
        node_name, string = consume(['[', ']'], string)
    except SyntaxError:
        return None # parser detects none return and falls through to normal
    if node_name is None or arrow not in ["->", "<-"]:
        return None
    return arrow, in_ledge, node_name

"Parses HTML. Used for placing configurable values into the HTML before encoding and transmission to the client."

# reads and parses the HTML content of the file
def parse(filepath: str, *values: tuple) -> str:
    return quick(filepath).format(*values)

# parse, but without the parsing
def quick(filepath: str) -> str:
    with open(filepath, "r") as f:
        content = f.read()
        f.close()
    return content

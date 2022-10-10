"Parses HTML. Used for placing configurable values into the HTML before encoding and transmission to the client."

# import required libraries
import re

# reads and parses the HTML content of the file
def parse(filepath: str, *values: tuple) -> str:
    return quick(filepath).format(*values)

# parse, but without the parsing
def quick(filepath: str) -> str:
    with open(filepath, "r") as f:
        content = f.read()
        f.close()
    return content

# detects a url in the provided string
def contains_url(text: str) -> bool:
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))" #cancer
    urls = re.findall(regex, text)
    if len(urls) > 0:
        return True
    return False

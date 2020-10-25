from rich.markup import escape
from unicodeit import replace


def parse_text(txt):
    if "$" in txt:
        txt = txt.replace("$", "").strip()
        return replace(txt)
    else:
        return txt


def parse_paragraph(node):
    paragraph = ""
    for sub, ent in node.walker():
        if sub.t == "text":
            paragraph += sub.literal
    return escape(parse_text(paragraph))

from rich.markup import escape
from unicodeit import replace
from pyinspect._colors import lightorange, lightgreen2


def parse_text(txt):
    if "$" in txt:
        txt = txt.replace("$", "").strip()
        return replace(txt)
    else:
        return txt


def parse_paragraph(node, in_list=False):
    paragraph = ""
    for sub, ent in node.walker():
        if sub.t == "text":
            paragraph += sub.literal
        elif sub.t == "code":
            paragraph += f"`{sub.literal}`"

    paragraph = parse_text(paragraph)

    if paragraph.strip().startswith("[ ]"):
        color = lightorange
    elif paragraph.strip().startswith("[x]"):
        color = lightgreen2
    else:
        color = None

    return escape(paragraph), color

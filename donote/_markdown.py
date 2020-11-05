from rich.markup import escape
from unicodeit import replace
from pyinspect._colors import lightorange, lightgreen2, lightgray
from pyinspect.utils import stringify
from rich.syntax import Syntax

HANDLED = (
    "text",
    "paragraph",
    "strong",
    "code",
    "code_block",
    "list",
    "document",
    "heading",
    "block_quote",
    "html_inline",
    "item",
    "html_block",
)


def parse_text(txt):
    if "$" in txt:
        txt = txt.replace("$", "").strip()
        return replace(txt)
    else:
        return txt


def parse_paragraph(node, in_list=False):
    paragraph = ""
    for sub, ent in node.walker():
        if sub.t in ("text"):
            txt = stringify(sub.literal, maxlen=-1).strip()
            paragraph += txt if txt != "None" else ""
        elif sub.t in ("strong"):
            txt = stringify(sub.literal, maxlen=-1).strip()
            paragraph += f"[b]{txt}[/b]" if txt != "None" else ""
        elif sub.t in ("italic"):
            txt = stringify(sub.literal, maxlen=-1).strip()
            paragraph += f"[i]{txt}[/i]" if txt != "None" else ""
        elif sub.t == "code":
            txt = stringify(
                Syntax(sub.literal, lexer_name="python"), maxlen=-1
            ).strip()
            paragraph += f"`{txt}`"

    paragraph = parse_text(paragraph)

    if paragraph.strip().startswith("[ ]"):
        color, style = lightorange, None
    elif paragraph.strip().startswith("[x]"):
        color, style = lightgreen2, "dim"
    else:
        color, style = None, None

    return (
        escape(paragraph).replace("[]", "[ ]").replace("]", "] "),
        color,
        style,
    )


def parse_block_quote(node):
    txt, color, _ = parse_paragraph(node)

    return txt, f"[dim {color}]" if color is not None else "[dim]"


def parse_html_block(node):
    txt = ""
    for sub, ent in node.walker():
        txt += sub.literal + "\n"
    return txt if not txt.startswith("<!--") else f"[dim green]{txt}"


def parse_html_inline(node):
    txt = ""
    for sub, ent in node.walker():
        txt += sub.literal
    return f"[{lightgray}]{txt}"

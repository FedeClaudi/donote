from rich.markdown import Markdown
from rich import print
from rich.panel import Panel
from pyinspect import Report
from random import choice
from pyinspect._colors import (
    lightred,
    orange,
    lightorange,
    green,
    dimgreen,
    lightgreen2,
    gray,
    lilla,
    yellow,
    salmon,
    mocassin,
)

from ._notes import _get_note_path, note_editor
from ._metadata import make_note_metadata, get_note_metadata, save_metadata
from ._markdown import parse_paragraph

blackboard = "#1f1f1f"
colors = [
    lightred,
    orange,
    lightorange,
    green,
    dimgreen,
    lightgreen2,
    gray,
    lilla,
    yellow,
    salmon,
    mocassin,
]


class Note:
    def __init__(self, note_name, raise_error=True):
        self.path = _get_note_path(note_name, raise_error=raise_error)
        self.name = note_name

        try:
            self._get_content()
        except FileNotFoundError as e:
            if raise_error:
                raise FileNotFoundError(e)

    def _get_content(self):
        with open(self.path, "r") as f:
            self.raw_content = f.read()
        self.content = Markdown(self.raw_content, inline_code_lexer="python")
        self.metadata = get_note_metadata(self.name)

    @property
    def tags(self):
        return self.metadata["tags"]

    @property
    def tags_render(self):
        tags = self.metadata["tags"]
        if not tags:
            return [
                Panel.fit("no tags", border_style=blackboard, padding=(-1, 1))
            ]
        else:
            tt = []
            for tag in tags:
                col = choice(colors)
                tt.append(
                    Panel.fit(
                        tag, border_style=col, padding=(-1, 1), style=col
                    )
                )

            return tt

    def add_tag(self, *tags):
        for tag in tags:
            if not isinstance(tag, str):
                raise TypeError("tag must be a string")

            if tag not in self.metadata["tags"]:
                self.metadata["tags"].append(tag)

    def pop_tag(self, *tags):
        for tag in tags:
            if tag in self.metadata["tags"]:
                idx = self.metadata["tags"].index(tag)
                self.metadata["tags"].pop(idx)

    @classmethod
    def from_string(cls, string, name):
        note = cls(name, raise_error=False)
        note.raw_content = string

        # make empty metadata
        note.metadata = make_note_metadata(name)

        return note

    def save(self):
        with open(self.path, "w") as out:
            out.write(self.raw_content)
        save_metadata(self.name, self.metadata)

        print(
            f"[{mocassin}]:ok_hand:  Saved note as: [{orange}]{self.path.name}"
        )

    def edit(self):
        note_editor(self.path)
        self._get_content()

    def show(self):
        show = Report(show_info=True, color=orange, accent=orange,)
        show._type = f":pencil:  {self.name}"

        in_list, first_header = False, True
        for current, entering in self.content.parsed.walker():
            node_type = current.t
            if node_type in ("heading") and entering:
                if not first_header:
                    show.spacer(2)
                show.add(f"[b {orange}]{current.first_child.literal}")
                show.spacer()
                first_header = False

            elif node_type in ("list") and entering:
                in_list = True
                for sub, ent in current.walker():
                    if sub.t == "paragraph" and ent:
                        paragraph, color = parse_paragraph(sub)
                        show.add(
                            f"- {paragraph}"
                            if color is None
                            else f"[{color}]- {paragraph}"
                        )

            elif node_type in ("list") and not entering:
                in_list = False
                show.spacer()

            elif node_type in ("paragraph") and entering and not in_list:
                paragraph, color = parse_paragraph(current)
                show.add(
                    f"{paragraph}"
                    if color is None
                    else f"[{color}]{paragraph}"
                )

            elif node_type == "softbreak":
                show.spacer()

            elif node_type == "code_block":
                show.spacer()
                language = current.info if current.info else "python"
                show.add(current.literal, "code", language=language)
                show.spacer()

        show.print()

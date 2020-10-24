from rich.markdown import Markdown
from rich import print
from pyinspect import Report
from pyinspect._colors import orange, mocassin

from ._notes import _get_note_path


class Note:
    def __init__(self, note_name, raise_error=True):
        self.path = _get_note_path(note_name, raise_error=raise_error)
        self.name = self.path.name

        try:
            with open(self.path, "r") as f:
                self.raw_content = f.read()

            self.content = Markdown(self.raw_content)  # for rich printing
        except FileNotFoundError as e:
            if raise_error:
                raise FileNotFoundError(e)

    @classmethod
    def from_string(cls, string, name):
        note = cls(name, raise_error=False)
        note.raw_content = string
        return note

    def save(self):
        with open(self.path, "w") as out:
            out.write(self.raw_content)
        print(f"[green]Saved note at: {self.path}")

    def show(self):
        show = Report(
            title=f"[b]{self.name}",
            show_info=True,
            color=mocassin,
            accent=orange,
        )
        show._type = self.name

        # Iterate over note content
        nodes = self.content.parsed.walker()
        for n, (current, entering) in enumerate(nodes):
            ntype = current.t
            if current.first_child is None or not entering:
                continue

            if ntype in ("text", "paragraph"):
                show.add(current.first_child.literal)

            elif ntype == "heading":
                if n > 0:
                    show.spacer()
                show.add(f"[bold {orange}]{current.first_child.literal}")

        show.print()

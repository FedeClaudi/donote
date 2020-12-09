from pyinspect import Report
from pyinspect._colors import orange, mocassin
from rich.bar import Bar
from rich.color import Color

from .note import Note
from ._metadata import make_note_metadata


class Todo(Note):
    def __init__(self, note_name, raise_error=True):
        """
            A special type of note for Todo lists.
        """
        Note.__init__(self, note_name, raise_error=raise_error)

        try:
            self.metadata["is_todo"] = True
        except AttributeError:
            self.metadata = make_note_metadata(note_name)
            self.metadata["is_todo"] = True

    @classmethod
    def from_string(cls, string, name):
        note = cls(name, raise_error=False)
        note.raw_content = string

        # make empty metadata
        note.metadata = make_note_metadata(name)

        return note

    def number_of_tasks(self):
        self.raw_content.replace("-[", "- [")

        completed = self.raw_content.count("- [x]")
        todo = self.raw_content.count("- [ ]")
        return completed + todo, completed, todo

    def show(self):
        show = Report(
            title=f"Todo list: [b]{self.name}",
            show_info=True,
            color=orange,
            accent=orange,
        )
        show._type = f":memo:  {self.name}"
        show.width = 120

        # Show the number of tasks in the note
        tot, completed, todo = self.number_of_tasks()
        n = completed / tot * 200
        color = Color.from_rgb(200 - n, n, 0)
        show.add(
            f"[{mocassin}]Completed[/{mocassin}] [b {orange}]{completed}/{tot}[/b {orange}][{mocassin}] tasks"
        )

        n = completed / tot * 200
        color = Color.from_rgb(200 - n, n, 0)
        bar = Bar(
            size=tot, begin=0, end=completed, color=color, bgcolor="#1a1a1a"
        )
        show.add(bar, "rich")

        # parse note content
        show.spacer()
        show.add("Tasks:")
        show = self._parse_content(show)
        show.spacer()

        # print
        show.print()

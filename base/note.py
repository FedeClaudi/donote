from rich.markdown import Markdown
from rich import print
from pyinspect import Report, what
from pyinspect._colors import orange, mocassin
import tempfile

from ._notes import _get_note_path


def create_note_interactive(note_name):
    path = _get_note_path(note_name)
    if path.exists():
        print(f'[{orange}]A note with name {note_name} already exists.')
        if Confirm.ask(f"Overwrite {path.name}?", default=False):
            print('Okay, not overwriting')
            return

    # Create a new note in a temp file, use nano to edit it and
    # then save to makrdown: https://stackoverflow.com/questions/3076798/start-nano-as-a-subprocess-from-python-capture-input

class Note:
    def __init__(self, note_name):
        self.path = _get_note_path(note_name)
        self.name = self.path.name

        with open(self.path, 'r') as f:
            self.raw_content = f.read()

        self.content = Markdown(self.raw_content)

    def show(self):
        show = Report(title=f'[b]{self.name}', show_info=True, color=mocassin, accent=orange)
        show._type = self.name

        # Iterate over note content
        nodes = self.content.parsed.walker()
        inlines = self.content.inlines
        new_line = False
        for n, (current, entering) in enumerate(nodes):
            ntype = current.t
            if current.first_child is None or not entering:
                continue
            
            if ntype in ('text', 'paragraph'):
                show.add(current.first_child.literal)


            elif ntype == 'heading':
                if n > 0: show.spacer()
                show.add(f'[bold {orange}]{current.first_child.literal}')

        show.print()
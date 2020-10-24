from pyinspect import Report
from pyinspect._colors import mocassin
from rich.table import Table
from rich.box import SIMPLE_HEAVY

from ._notes import get_all_notes, get_note_metadata
from .note import Note

def open_note(note_name):
    return Note(note_name)


def make_new_note(note_name):
    with open(_get_note_path(note_name), 'w') as f:
        f.write('')


def list_notes():
    notes = get_all_notes()

    
    tb = Table(box=SIMPLE_HEAVY, header_style='bold green')
    tb.add_column(header='Name')
    tb.add_column(header='# lines', justify='center')
    tb.add_column(header='size', justify='center')
    tb.add_column(header='last edited', justify='center')
    tb.add_column(header='created', style='dim', justify='center')

    for note in notes:
        created, edited, size, num_lines = get_note_metadata(note)
        tb.add_row(f'[b {mocassin}]{note}', num_lines, size, edited, created)

    panel = Report(title='Notes')
    panel.add(tb, 'rich')
    panel.print()
    
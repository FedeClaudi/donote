from pyinspect import Report
from pyinspect._colors import mocassin, orange
from rich.table import Table
from rich.box import SIMPLE_HEAVY
import sys
import tempfile
import subprocess
import os
from rich import print
from rich.prompt import Confirm
from pyinspect import what

from ._notes import get_all_notes, get_note_metadata, _get_note_path
from .note import Note
from .paths import windows

def open_note(note_name):
    return Note(note_name)

def create_note_interactive(note_name):
    print(f'[{mocassin}]Making a new note: [{orange}]{note_name}')

    path = _get_note_path(note_name, raise_error=False)
    if path.exists():
        print(f'[{orange}]A note with name {note_name} already exists.')
        if not Confirm.ask(f"Overwrite {path.name}?", default=False):
            print('Okay, not overwriting')
            return

    # Create temp file to write note
    temp =  tempfile.NamedTemporaryFile(mode='w+t', delete=False)
    try:
        if not windows:
            subprocess.call(['nano', temp.name])
        else:
            subprocess.call(['C:\\Program Files\\Git\\usr\\bin\\nano.exe', temp.name])
    except  Exception:
        print('[red]Failed to crate note in interactive mode, creating empyt note')
        return create_new_note(note_name)
        
    # Read temp content and close
    with open(temp.name) as f: 
        content = f.read()
    temp.close()
    os.unlink(temp.name)


    # Save note to file
    Note.from_string(content, note_name).save()

      

def create_new_note(note_name):
    print(f'[{mocassin}]Making a new empty note: [{orange}]{note_name}')

    path = _get_note_path(note_name)
    if path.exists():
        print(f'[{orange}]A note with name {note_name} already exists.')
        if Confirm.ask(f"Overwrite {path.name}?", default=False):
            with open(path, 'w') as f:
                f.write('')

    print(f'[{mocassin}]    saved note at: [{orange}]{note_name}')


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
    
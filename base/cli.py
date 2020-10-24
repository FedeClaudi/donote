from rich import print
import click
from pyinspect._colors import orange, mocassin

from .notes import make_new_note, open_note, list_notes

def make(new_note):
    print(f'[{mocassin}]Making a new note: [{orange}]{new_note}')
    make_new_note(new_note)

def show(note_name):
    note = open_note(note_name)
    content = note.read()
    print(content)

@click.command()
@click.option('-n', '--new', 'new_note')
@click.option('-o', '--open', 'to_open')
@click.option('-s', '--show', 'to_show')
@click.option('-l', is_flag=True)
def cli_main(new_note, to_open, to_show, l=False):

    if new_note is not None:
        make(new_note)

    if to_show:
        open_note(to_show).show()
        
    if l:
        list_notes()


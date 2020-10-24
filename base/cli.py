from rich import print
import click
import sys
from pyinspect._colors import orange, mocassin

from .notes import create_new_note, create_note_interactive, open_note, list_notes

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
        create_note_interactive(new_note)


    if to_show:
        open_note(to_show).show()
        
    if l:
        list_notes()


from pyinspect._colors import mocassin, orange
from rich.table import Table
from rich.box import SIMPLE_HEAVY
from rich.prompt import Confirm
from rich import print
from pyinspect.utils import dir_files

from ._notes import (
    get_note_file_metadata,
    _get_note_path,
    note_editor,
)
from .note import Note
from .paths import notes_folder
from ._metadata import _get_note_metadata_path


def open_note(note_name):
    try:
        return Note(note_name)
    except Exception:
        if Confirm.ask("No note found, create a new one?", default=True):
            create_note_interactive(note_name)


def show_note(note_name):
    Note(note_name).show()


def edit_note(note_name):
    Note(note_name).edit()


def get_all_notes():
    notes = dir_files(notes_folder, pattern="*.md")
    return [open_note(n.name) for n in notes]


def create_note_interactive(note_name):
    print(f"[{mocassin}]Making a new note: [{orange}]{note_name}")

    path = _get_note_path(note_name, raise_error=False)
    if path.exists():
        print(f"[{orange}]A note with name {note_name} already exists.")
        if not Confirm.ask(f"Overwrite {path.name}?", default=False):
            print("Okay, not overwriting")
            return

    # Create a live editor to fill in note content
    try:
        content = note_editor()
    except Exception:
        print(f"[{orange}]Creating empty note instead")
        return create_new_note(note_name)

    # Save note to file
    Note.from_string(content, note_name).save()


def create_new_note(note_name):
    print(f"[{mocassin}]Making a new empty note: [{orange}]{note_name}")

    path = _get_note_path(note_name)
    if path.exists():
        print(f"[{orange}]A note with name {note_name} already exists.")
        if Confirm.ask(f"Overwrite {path.name}?", default=False):
            Note.from_string("", note_name).save()

    print(f"[{mocassin}]    saved note at: [{orange}]{note_name}")


def delete_note(note_name):
    path = _get_note_path(note_name)
    metadata_path = _get_note_metadata_path(note_name)

    if Confirm.ask(
        f"[{mocassin}]Deleting note: [{orange}]{note_name}[/{orange}], continue?",
        default=False,
    ):
        path.unlink()
        metadata_path.unlink()
        print(f"    [{mocassin}]removed: [{orange}]{note_name}")


def list_notes():

    tb = Table(header_style="bold green", box=SIMPLE_HEAVY)
    tb.add_column(header="Name", width=15)
    tb.add_column(header="# lines", justify="center", width=8)
    tb.add_column(header="size", justify="center", width=12)
    tb.add_column(header="edited", justify="center", width=12)
    tb.add_column(header="created", style="dim", justify="center", width=12)
    tb.add_column(header="tags")

    notes = get_all_notes()
    for note in notes:
        name, created, edited, size, num_lines = get_note_file_metadata(
            note.name
        )
        name.style = f"bold {mocassin}"

        tb.add_row(name, num_lines, size, edited, created, *note.tags_render)
    print(tb)

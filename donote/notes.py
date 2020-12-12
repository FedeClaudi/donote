from pyinspect._colors import mocassin, orange
from rich.table import Table
from rich.box import SIMPLE_HEAVY
from rich.prompt import Confirm
from rich import print
from pyinspect.utils import dir_files, listdir
from pathlib import Path

from ._notes import (
    get_note_file_metadata,
    _get_note_path,
    note_editor,
)
from .note import Note
from .todo import Todo
from .paths import notes_folder
from ._metadata import _get_note_metadata_path


def show_file(filename):
    if not filename.endswith(".md"):
        raise ValueError(
            f"The file passed does not appear to be markdown: {filename}"
        )

    path = Path(filename)

    note = Note(path.name.replace(".md", ""), raise_error=False)
    note.path = path
    note._get_content(ignore_metadata=True)
    note.show()


def open_note(note_name, todo=False):
    try:
        note = Note(note_name) if not todo else Todo(note_name)
    except Exception:
        if Confirm.ask("No note found, create a new one?", default=True):
            note = create_note_interactive(note_name, todo=todo)
            return None
    else:
        try:
            if note.metadata["is_todo"] or todo:
                return Todo(note_name)
            else:
                return note
        except KeyError:
            return note  # for backward compatibility


def show_note(note_name, todo=False):
    n = open_note(note_name, todo=todo)
    if n is None:
        return
    n.show()
    return n


def show_note_html(note_name, todo=False):
    n = open_note(note_name, todo=todo)
    if n is None:
        return
    n.show_html()
    return n


def edit_note(note_name, todo=False):
    n = open_note(note_name, todo=todo)
    if n is None:
        return
    n.edit()
    n.save()
    print(f":pencil:  [{mocassin}]finished editing [{orange}]{note_name}")
    return show_note(note_name)


def tag_note(note_name, tag, **kwargs):
    n = open_note(note_name)
    n.add_tag(tag)
    n.save()
    print(f":ok_hand:  [{mocassin}]added tag to [{orange}]{note_name}")
    return n


def untag_note(note_name, tag, **kwargs):
    n = open_note(note_name)
    n.pop_tag(tag)
    n.save()
    print(f":ok_hand:  [{mocassin}]removed tag from [{orange}]{note_name}")
    return n


def get_all_notes():
    notes = dir_files(notes_folder, pattern="*.md")
    return [open_note(n.name) for n in notes]


def create_note_interactive(note_name, todo=False):
    print(f"[{mocassin}]Making a new note: [{orange}]{note_name}")

    path = _get_note_path(note_name, raise_error=False)
    if path.exists():
        print(f"[{orange}]A note with name {note_name} already exists.")
        if not Confirm.ask(f"Overwrite {path.name}?", default=False):
            print("Okay, not overwriting")
            return

    # Create a live editor to fill in note content
    content = note_editor()

    # Save note to file
    if not todo:
        note = Note.from_string(content, note_name)
    else:
        note = Todo.from_string(content, note_name)
    note.save()

    return note


def create_new_note(note_name, todo=False):
    print(f"[{mocassin}]Making a new empty note: [{orange}]{note_name}")

    path = _get_note_path(note_name, raise_error=False)
    if path.exists():
        print(f"[{orange}]A note with name {note_name} already exists.")
        if not Confirm.ask(f"Overwrite {path.name}?", default=False):
            print(f"[{mocassin}]    okay, not saving then.")
            return

    if not todo:
        note = Note.from_string("", note_name)
    else:
        note = Todo.from_string("", note_name)
    note.save()

    print(f"[{mocassin}]    saved note at: [{orange}]{note_name}")
    return note


def delete_note(note_name, force=False, **kwargs):
    path = _get_note_path(note_name)
    metadata_path = _get_note_metadata_path(note_name)

    if not force:
        confirm = Confirm.ask(
            f"[{mocassin}]Deleting note: [{orange}]{note_name}[/{orange}], continue?",
            default=False,
        )

    if force or confirm:
        path.unlink()
        metadata_path.unlink()
        print(f"    [{mocassin}]removed: [{orange}]{note_name}")


def list_notes(list_files=False, **kwargs):

    tb = Table(header_style="bold green", box=SIMPLE_HEAVY, min_width=88)
    tb.add_column(header="Name", min_width=20)
    tb.add_column(header="# lines", justify="center", min_width=8)
    tb.add_column(header="size", justify="center", min_width=16)
    tb.add_column(header="edited", justify="center", min_width=16)
    tb.add_column(
        header="created", style="dim", justify="center", min_width=16
    )
    tb.add_column(header="tags")

    notes = get_all_notes()
    for note in notes:
        name, created, edited, size, num_lines = get_note_file_metadata(
            note.name
        )
        name.style = f"bold {mocassin}"

        tb.add_row(name, num_lines, size, edited, created, *note.tags_render)

    print(tb)

    if list_files:
        listdir(notes_folder, extension="md")

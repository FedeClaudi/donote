from pyinspect.utils import dir_files
from rich.filesize import decimal as format_size
import sys
import tempfile
import subprocess
import os
from pathlib import Path
from rich import print
from .paths import windows

from .paths import notes_folder
from .utils import format_timestamp


def _get_note_path(note_name, raise_error=True):
    if ".md" not in note_name:
        note_name += ".md"
    path = notes_folder / note_name
    if not path.exists() and raise_error:
        raise FileNotFoundError(f"Could not find note with name {note_name}")
    return path


def note_editor(file_path=None):
    # Create temp file to write note
    if file_path is None:
        temp = tempfile.NamedTemporaryFile(mode="w+t", delete=False)
        file_path = temp.name
        cleanup = True
    else:
        file_path = Path(file_path)
        cleanup = False
        if not file_path.exists():
            raise FileNotFoundError(
                f"Could not open note editor, file not found: {file_path}"
            )

    try:
        if not windows:
            subprocess.call(["nano", file_path])
        else:
            subprocess.call(
                ["C:\\Program Files\\Git\\usr\\bin\\nano.exe", file_path]
            )
    except Exception as e:
        print(f"[red]Failed to open note editor: {e}")
        return None

    # Read temp content and close
    with open(file_path) as f:
        content = f.read()

    if cleanup:
        temp.close()
        os.unlink(temp.name)

    return content


def get_all_notes():
    notes = dir_files(notes_folder, pattern="*.md")
    return [n.name for n in notes]


def get_note_metadata(note_name):
    stats = _get_note_path(note_name).stat()

    if sys.platform == "Win32":
        created = format_timestamp(stats.st_ctime)
    else:
        try:
            created = format_timestamp(stats.st_birthtime)
        except AttributeError:
            # no easy way to do this in Linux
            created = ""

    edited = format_timestamp(stats.st_mtime)

    size = format_size(stats.st_size)

    num_lines = str(sum(1 for line in open(_get_note_path(note_name))))
    return created, edited, size, num_lines

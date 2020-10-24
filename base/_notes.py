from pyinspect.utils import dir_files
from datetime import datetime
from pyinspect import what
from rich.filesize import decimal as format_size
import sys

from .paths import notes_folder
from .utils import format_timestamp

def _get_note_path(note_name):
    if '.md' not in note_name:
        note_name += '.md'
    path = notes_folder/note_name
    if not path.exists():
        raise FileNotFoundError(f'Could not find note with name {note_name}')
    return path

def get_all_notes():
    notes = dir_files(notes_folder, pattern='*.md')
    return [n.name for n in notes]


def get_note_metadata(note_name):
    stats = _get_note_path(note_name).stat()

    if sys.platform == 'Win32':
        created = format_timestamp(stats.st_ctime)
    else:
        try:
            created = format_timestamp(stats.st_birthtime)
        except AttributeError:
            # no easy way to do this in Linux
            created = ''

    edited = format_timestamp(stats.st_mtime)

    size = format_size(stats.st_size)

    num_lines = str(sum(1 for line in open(_get_note_path(note_name))))
    return created, edited, size, num_lines
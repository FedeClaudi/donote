from pyinspect import install_traceback

install_traceback()


from .note import Note
from .notes import (
    open_note,
    create_new_note,
    list_notes,
    create_note_interactive,
    delete_note,
    edit_note,
)

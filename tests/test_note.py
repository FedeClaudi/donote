from donote.notes import (
    create_new_note,
    open_note,
    list_notes,
    delete_note,
    show_note,
)
from donote.note import Note


def test_create_note():
    create_new_note("testing")


def test_open_note():
    note = open_note("testing")
    if not isinstance(note, Note):
        raise AssertionError


def test_note_attributes():
    note = open_note("testing")

    note.name == "testing"
    note.raw_content = ""


def test_tags():
    note = open_note("testing")
    assert note.tags == []

    note.add_tag("test")
    assert note.tags == ["test"]

    note.pop_tag("test")
    assert note.tags == []


def test_note_save():
    note = open_note("testing")
    note.save()


def test_note_show():
    note = open_note("testing")
    note.show()

    show_note("testing")


def test_list_notes():
    list_notes()


def test_delete_note():
    delete_note("testing", force=True)

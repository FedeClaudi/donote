import click
from .notes import (
    create_note_interactive,
    open_note,
    list_notes,
    delete_note,
    show_note,
    edit_note,
    tag_note,
    untag_note,
)

commands = dict(
    show=show_note,
    remove=delete_note,
    rm=delete_note,
    delete=delete_note,
    open=open_note,
    o=open_note,
    add=create_note_interactive,
    new=create_note_interactive,
    n=create_note_interactive,
    e=edit_note,
    edit=edit_note,
    t=tag_note,
    tag=tag_note,
    untag=untag_note,
)


@click.command()
@click.argument("command")
@click.argument("note_name", default=None, required=False)
@click.argument("tag", default=None, required=False)
def cli_main(command, note_name, tag):
    if command == "list" or command == "l":
        list_notes()
    else:
        if note_name is None:
            raise ValueError("No note name passed")

        try:
            if not tag:
                commands[command](note_name)
            else:
                commands[command](note_name, tag)
        except KeyError:
            raise ValueError(f"Command {command} is not recognized.")

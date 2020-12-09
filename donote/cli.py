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
    show_file,
    show_note_html,
)

commands = dict(
    show=show_note,
    s=show_note,
    sh=show_note_html,
    show_html=show_note_html,
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
    sf=show_file,
    showfile=show_file,
)


@click.command()
@click.argument("command")
@click.argument("note_name", default=None, required=False)
@click.argument("tag", default=None, required=False)
@click.option("--todo", is_flag=True)
def cli_main(command, note_name, tag, todo):
    if command == "list" or command == "l":
        list_notes()
    else:
        if note_name is None:
            raise ValueError("No note name passed")

        try:
            if not tag:
                commands[command](note_name, todo=todo)
            else:
                commands[command](note_name, tag, todo=todo)
        except KeyError:
            raise ValueError(f"Command {command} is not recognized.")

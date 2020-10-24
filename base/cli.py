import click
from .notes import (
    create_note_interactive,
    open_note,
    list_notes,
    delete_note,
)


@click.command()
@click.option("-n", "--new", "new_note")
@click.option("-o", "--open", "to_open")
@click.option("-s", "--show", "to_show")
@click.option("-rm", "--remove", "to_remove")
@click.option("-lst", is_flag=True)
def cli_main(new_note, to_open, to_show, to_remove, lst=False):

    if new_note is not None:
        create_note_interactive(new_note)

    if to_show:
        open_note(to_show).show()

    if to_remove:
        delete_note(to_remove)

    if lst:
        list_notes()

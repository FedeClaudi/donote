import json

from .paths import note_metadata_folder

_metadata_template = dict(name="", tags=[],)


def _get_note_metadata_path(note_name, raise_error=True):
    note_name = note_name.replace(".md", "")
    if ".json" not in note_name:
        note_name += ".json"

    path = note_metadata_folder / note_name
    if not path.exists() and raise_error:
        raise FileNotFoundError(
            f"Could not find note metadata file for {note_name}"
        )
    return path


def make_note_metadata(note_name, name=None, tags=None):
    metadata = _metadata_template.copy()
    metadata["name"] = name if name is not None else ""

    if tags is not None and not isinstance(tags, list):
        tags = [tags]
    metadata["tags"] = tags if tags is not None else []

    return metadata


def save_metadata(note_name, metadata):
    path = _get_note_metadata_path(note_name, raise_error=False)
    with open(path, "w") as jfile:
        json.dump(metadata, jfile)


def get_note_metadata(note_name):
    path = _get_note_metadata_path(note_name)
    with open(path, "r") as jfile:
        meta = json.load(jfile)
    return meta

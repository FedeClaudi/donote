import sys
from pathlib import Path

if sys.platform == "win32":
    windows = True
    base_folder = Path("D:\\Dropbox (UCL - SWC)\\Rotation_vte\\knowledge_base")
else:
    windows = False
    base_folder = Path(
        "/Users/federicoclaudi/Dropbox (UCL)/Rotation_vte/knowledge_base"
    )

# Make subdirs
notes_folder = base_folder / "notes"
note_metadata_folder = base_folder / ".notes_metadata"

notes_folder.mkdir(exist_ok=True)
note_metadata_folder.mkdir(exist_ok=True)

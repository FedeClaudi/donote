import sys
from pathlib import Path

if sys.platform == 'win32':
    raise NotImplementedError
else:
    base_folder = Path('/Users/federicoclaudi/Dropbox (UCL)/Rotation_vte/knowledge_base')

# Make subdirs
notes_folder = base_folder / 'notes'
notes_folder.mkdir(exist_ok=True)
import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path


current_dir = os.getcwd()
home_dir = str(Path.home())

if current_dir != '{}/core'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core')

EDITOR = os.environ.get('EDITOR','vim')

all_note_folders = os.listdir('personal/project_notes')

full_note_path = 'personal/project_notes/TEMPTASKDOC'

if 'TEMPTASKDOC' in os.listdir('personal/project_notes'):
    with open(full_note_path, 'r') as _in:
        call([EDITOR, _in.name])
else:
    with open(full_note_path, 'w') as _in:
        call([EDITOR, _in.name])


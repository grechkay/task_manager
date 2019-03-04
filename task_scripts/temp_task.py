import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path


current_dir = os.getcwd()
home_dir = str(Path.home())
project_notes_path = '{}/core/personal/project_notes'.format(home_dir)

EDITOR = os.environ.get('EDITOR','vim')

all_note_folders = os.listdir(project_notes_path)

full_note_path = '{}/core/personal/project_notes/TEMPTASKDOC'.format(home_dir)

if 'TEMPTASKDOC' in os.listdir(project_notes_path):
    with open(full_note_path, 'r') as _in:
        call([EDITOR, _in.name])
else:
    with open(full_note_path, 'w') as _in:
        call([EDITOR, _in.name])


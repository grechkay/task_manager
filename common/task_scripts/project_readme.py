import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path

# First argument is the project

current_dir = os.getcwd()
home_dir = str(Path.home())

if current_dir != '{}/core/common'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core/common')

project = sys.argv[1]
EDITOR = os.environ.get('EDITOR','vim')

all_note_folders = os.listdir('project_notes')
if project not in all_note_folders:
    call(['mkdir', 'project_notes/{}'.format(project)])

full_note_path = 'project_notes/{project}/README'.format(
        project=project,
)

if 'README' in os.listdir('project_notes/{}'.format(project)):
    with open(full_note_path, 'r') as _in:
        call([EDITOR, _in.name])
else:
    with open(full_note_path, 'w') as _in:
        call([EDITOR, _in.name])


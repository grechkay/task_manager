import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime

# First argument is the project

project = sys.argv[1]
EDITOR = os.environ.get('EDITOR','vim')

all_note_folders = os.listdir('project_notes')
if project not in all_note_folders:
    call(['mkdir', 'project_notes/{}'.format(project)])

full_note_path = 'project_notes/{project}/README'.format(
        project=project,
)

with open(full_note_path, 'r') as _in:
    call([EDITOR, _in.name])


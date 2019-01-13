import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path
from jsonpath import jsonpath
from taskw import TaskWarrior

# First argument is the project

current_dir = os.getcwd()
home_dir = str(Path.home())
w = TaskWarrior()
tasks = w.load_tasks()

if current_dir != '{}/core/common'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core/common')

project = sys.argv[1]
EDITOR = os.environ.get('EDITOR','vim')

full_dir_path = project
project_id = jsonpath(tasks, "$..[?(@.description=='{project}')].uuid".format(project=project))
current_id = jsonpath(tasks, "$..[?(@.depends=='{}')].uuid".format(project_id[0]))

while current_id:
    parent_project = jsonpath(tasks, "$..[?(@.uuid=='{}')].description".format(current_id[0]))
    full_dir_path = '{project}/{path}'.format(project=parent_project[0],path=full_dir_path)
    current_id = jsonpath(tasks, "$..[?(@.depends=='{}')].uuid".format(current_id[0]))

full_dir_path = 'project_notes/{path}'.format(path=full_dir_path)

call(['mkdir', '-p', full_dir_path])
full_note_path = '{path}/README'.format(path=full_dir_path)

if 'README' in os.listdir(full_dir_path):
    with open(full_note_path, 'r') as _in:
        call([EDITOR, _in.name])
else:
    with open(full_note_path, 'w') as _in:
        call([EDITOR, _in.name])


import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime

# First argument is the project
# Second argument is the title/description

def get_task_id(project):
    w = TaskWarrior()
    tasks = w.load_tasks()['pending']
    for task in tasks:
        if task['project'] == project and 'main' in task['tags']:
            return task['id']
    
project = sys.argv[1]
description = sys.argv[2]
EDITOR = os.environ.get('EDITOR','vim')

date = datetime.strftime(datetime.now(),'%Y-%m-%d')
task_id = get_task_id(project)

all_note_folders = os.listdir('task_notes')
if project not in all_note_folders:
    call(['mkdir', 'task_notes/{}'.format(project)])

all_months = os.listdir('task_notes/{}'.format(project))
if date[:7] not in all_months:
    call(['mkdir', 'task_notes/{0}/{1}'.format(project, date[:7])])

all_notes = os.listdir('task_notes/{0}/{1}'.format(project, date[:7]))
note_number = 0

for note in all_notes:
    if date == note[:10]:
        note_number += 1

note_name = '{date}_{num}'.format(date=date, num=note_number)
full_note_path = 'task_notes/{project}/{month}/{name}'.format(
        project=project,
        month=date[:7],
        name=note_name,
)

with open(full_note_path, 'w') as _in:
    _in.write(description)
    _in.flush()
    call([EDITOR, _in.name])

call(['task', str(task_id), 'annotate', '{0}_{1}'.format(note_name, description)])

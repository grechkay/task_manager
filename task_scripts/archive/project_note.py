import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path
from jsonpath import jsonpath

# First argument is the project
# Second argument is the title/description

current_dir = os.getcwd()
home_dir = str(Path.home())
w = TaskWarrior()
tasks = w.load_tasks()

if current_dir != '{}/core'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core')

def get_task_id(project):
    project_id = jsonpath(tasks, "$..[?(@.description=='{project}')].id".format(project=project))
    return project_id[0]
    
project = sys.argv[1]
description = sys.argv[2]
EDITOR = os.environ.get('EDITOR','vim')

date = datetime.strftime(datetime.now(),'%Y-%m-%d')
task_id = get_task_id(project)

full_dir_path = '{project}/{month}'.format(project=project, month=date[:7])
project_id = jsonpath(tasks, "$..[?(@.description=='{project}')].uuid".format(project=project))
current_id = jsonpath(tasks, "$..[?('{}' in @.depends)].uuid".format(project_id[0]))

while current_id:
    parent_project = jsonpath(tasks, "$..[?(@.uuid=='{}')].description".format(current_id[0]))
    full_dir_path = '{project}/{path}'.format(project=parent_project[0],path=full_dir_path)
    current_id = jsonpath(tasks, "$..[?('{}' in @.depends)].uuid".format(current_id[0]))

full_dir_path = 'personal/project_notes/{path}'.format(path=full_dir_path)
call(['mkdir', '-p', full_dir_path])
print(full_dir_path)
all_notes = os.listdir(full_dir_path)
note_number = 0

for note in all_notes:
    if date == note[:10]:
        note_number += 1

note_name = '{date}_{num}_{desc}'.format(
        date=date, 
        num=note_number,
        desc=description,
)
full_note_path = '{path}/{name}'.format(path=full_dir_path, name=note_name)

with open(full_note_path, 'w') as _in:
    _in.write(description)
    _in.flush()
    call([EDITOR, _in.name])

call(['task', str(task_id), 'annotate', note_name])

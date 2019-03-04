import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path

# First argument is the project

current_dir = os.getcwd()
home_dir = str(Path.home())
track_path = '{}/core/personal'.format(home_dir)

track_target = sys.argv[1] #This is the target that is tracked
track_date = sys.argv[2] #This is the ds in the format: YYYY-MM-DD
track_value = sys.argv[3] #This is the value given to the tracked target


all_track_targets = os.listdir('{}/track_targets'.format(track_path))

if '{}.track'.format(track_target) not in all_track_targets:
    raise ValueError('Target is not tracked')

with open('{}/track_targets/{}.track'.format(track_path, track_target), 'a') as _in:
    _in.write('{ds},{val}\n'.format(ds=track_date, val=track_value))


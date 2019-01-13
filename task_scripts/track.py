import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path

# First argument is the project

current_dir = os.getcwd()
home_dir = str(Path.home())
current_ts = int(datetime.now().timestamp())

if current_dir != '{}/core'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core')

track_target = sys.argv[1] #This is the target that is tracked
track_value = sys.argv[2] #This is the value given to the tracked target


all_track_targets = os.listdir('personal/track_targets')

if '{}.track'.format(track_target) not in all_track_targets:
    raise ValueError('Target is not tracked')

with open('personal/track_targets/{}.track'.format(track_target), 'a') as _in:
    _in.write('{dt},{val}\n'.format(dt=current_ts, val=track_value))


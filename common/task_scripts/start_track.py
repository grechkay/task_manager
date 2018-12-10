import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path

# First argument is the project

current_dir = os.getcwd()
home_dir = str(Path.home())
current_ts = int(datetime.now().timestamp())

if current_dir != '{}/core/common'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core/common')

track_target = sys.argv[1] #This is the target that is tracked
min_value = sys.argv[2] #This is the min value of the tracked target (be conservative)
max_value = sys.argv[3] #This is the max value of the tracked target
direction = sys.argv[4] #up/down signifies which direction you want improvement

all_track_targets = os.listdir('track_targets')
if '{}.track'.format(track_target) in all_track_targets:
    raise ValueError('tracking already exists')

with open('track_targets/{}.track'.format(track_target), 'w') as _in:
    _in.write('{min},{max},{dir}\n'.format(min=min_value, max=max_value,dir=direction))
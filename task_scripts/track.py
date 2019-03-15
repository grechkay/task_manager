import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path

# First argument is the project

def show_error():
    print("\n\n\t\033[91mError. please execute \n\tpython goals.py [target] [YYYY-MM-DD] [value]\n")
    print("\033[0m")
    assert False

current_dir = os.getcwd()
home_dir = str(Path.home())
track_path = '{}/core/personal'.format(home_dir)
all_track_targets = os.listdir('{}/track_targets'.format(track_path))

if len(sys.argv) == 1:
	# show the track targets
	print("\nCurrent track targets:")
	for t in all_track_targets:
		print("\t" + t[: -len('.track')]) # so that the '.track' doesn't appear
	print()
	sys.exit()


if len(sys.argv) != 4:
    show_error()

track_target = sys.argv[1] #This is the target that is tracked
track_date = sys.argv[2] #This is the ds in the format: YYYY-MM-DD
track_value = sys.argv[3] #This is the value given to the tracked target

if track_date == 't': # today
    dt = datetime.now()
elif track_date == 'y': # yesterday
    dt = datetime.now() - timedelta(days=1)
elif track_date == 'tom': # tomorrow
    dt = datetime.now() + timedelta(dats=1)
else:
    try:
        dt = datetime.strptime(track_date, '%Y-%m-%d')
    except ValueError:
        show_error()
track_date = dt.strftime('%Y-%m-%d') # this will get the good format so even if user types '2019-3-14' it still works



if '{}.track'.format(track_target) not in all_track_targets:
    raise ValueError('Target is not tracked')

with open('{}/track_targets/{}.track'.format(track_path, track_target), 'a') as _in:
    _in.write('{ds},{val}\n'.format(ds=track_date, val=track_value))


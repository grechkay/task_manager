import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path
from datetime import datetime
from datetime import date
from collections import Counter
from datetime import timedelta
from project_manager import ProjectManager
from iso_info import get_iso_info

# First argument is the project

current_dir = os.getcwd()
home_dir = str(Path.home())
personal_dir = '{}/core/personal'.format(home_dir)
EDITOR = os.environ.get('EDITOR','vim')
pm = ProjectManager()

goal_date = sys.argv[1] #This is today's date
goal_timeframe = sys.argv[2] 
#This is the timeline of the goal: 
# y - year
# q - quarter
# m - month
# w - week
# d - day

# Everything will be based on the week, so the overlapping 
# days may be put into different quarters/months/years

dt = datetime.strptime(goal_date, '%Y-%m-%d')
iso_info = get_iso_info(dt)

timeframe_dict = {
    'yearly':1,
    'quarterly':2,
    'monthly':3,
    'weekly':4,
    'daily':4,
}
timeframe_number = timeframe_dict[goal_timeframe]

year = iso_info['year']
quarter = iso_info['quarter']
month = iso_info['month']
week = iso_info['week']

path_additions = {
    1:str(year),
    2:'q{}'.format(str(quarter)),
    3:'m{}'.format(str(month)),
    4:'w{}'.format(str(week)),
}
full_dir_path = '{}/goals'.format(personal_dir)
for i in range(1,timeframe_number + 1):
    full_dir_path += '/{}'.format(path_additions[i])

call(['mkdir', '-p', full_dir_path])
if goal_timeframe == 'daily':
    goal_name = goal_date
else:
    start_day = iso_info['{}_start'.format(goal_timeframe[:-2])]
    end_day = iso_info['{}_end'.format(goal_timeframe[:-2])]
    
    goal_name = '{}_goal_{}--{}'.format(goal_timeframe, start_day.date(), end_day.date())

default_string = \
"""
context for the goals:

min_goal:

goal:

stretch_goal:

evaluation of the goals:
"""

pm.modify_file(
    goal_name,
    full_dir_path,
    default_string,
)


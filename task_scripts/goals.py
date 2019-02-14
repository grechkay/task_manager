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

# First argument is the project

current_dir = os.getcwd()
home_dir = str(Path.home())
EDITOR = os.environ.get('EDITOR','vim')
pm = ProjectManager()

if current_dir != '{}/core'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core')

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

year = int(goal_date[:4])
month = int(goal_date[5:7])
day = int(goal_date[8:10])
date_from = date(year-1, 12, 31)
date_to = date(year, month, day)
delta = (date_to - date_from).days
day_delta = timedelta(days=1)
timeframe_dict = {
    'yearly':1,
    'quarterly':2,
    'monthly':3,
    'weekly':4,
    'daily':4,
}
timeframe_number = timeframe_dict[goal_timeframe]

def check_num_mondays(d1, d2):
    num_mondays = 0
    for i in range(1, delta+1):
        check_date = date_from + day_delta * i
        if check_date.strftime('%a') == 'Mon':
            num_mondays += 1
    return num_mondays

num_mondays = check_num_mondays(date_from, date_to)

if num_mondays == 0:
    last_year = date(year-2,12,31)
    last_year_mondays = check_num_mondays(last_year, date_from)

    year = year - 1
    quarter = 4
    month = 12
    week = last_year_mondays
else:
    quarter = min((num_mondays-1) // 13 + 1, 4)
    month = min((num_mondays-1) // 4 + 1, 12) 
    week = num_mondays

path_additions = {
    1:str(year),
    2:'q{}'.format(str(quarter)),
    3:'m{}'.format(str(month)),
    4:'w{}'.format(str(week)),
}
full_dir_path = 'personal/goals'
for i in range(1,timeframe_number + 1):
    full_dir_path += '/{}'.format(path_additions[i])

call(['mkdir', '-p', full_dir_path])
if goal_timeframe == 'daily':
    goal_name = goal_date
else:
    goal_name = '{}_goal'.format(goal_timeframe)

default_string = """min_goal:

goal:

stretch_goal:
"""

pm.modify_file(
    goal_name,
    full_dir_path,
    default_string,
)


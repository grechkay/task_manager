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

goal_date = sys.argv[1] #This is date you want the report for
goal_timeframe = 'daily'
dt = datetime.strptime(goal_date, '%Y-%m-%d')

#This is the timeline of the goal: 
# y - year
# q - quarter
# m - month
# w - week
# d - day

# Everything will be based on the week, so the overlapping 
# days may be put into different quarters/months/years

iso_info = get_iso_info(dt)
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

goal_strings = [
    '',
    'yearly goals from {} to {}\n\n'.format(iso_info['year_start'].date(), iso_info['year_end'].date()),
    'quarterly goals from {} to {}\n\n'.format(iso_info['quarter_start'].date(), iso_info['quarter_end'].date()),
    'monthly goals from {} to {}\n\n'.format(iso_info['month_start'].date(), iso_info['month_end'].date()),
    'weekly goals from {} to {}\n\n'.format(iso_info['week_start'].date(), iso_info['week_end'].date())
]

full_dir_path = '{}/goals'.format(personal_dir)
report_string = ""
underscore = '_'*80 + '\n'

for i in range(1, 5):
    full_dir_path += '/{}'.format(path_additions[i])
    files = os.listdir(full_dir_path)
    for _file in files:
        if 'goal' in _file:
            report_string += goal_strings[i]
            file_path = '{}/{}'.format(full_dir_path, _file)
            with open(file_path, 'r') as _in:
                for line in _in:
                    report_string += line

            report_string += underscore
    

files = os.listdir(full_dir_path)
files = sorted(files)


if 'goal' in files[-1]:
    files.pop()

for _file in files:
    report_string += '{}\n\n'.format(_file)
    file_path = '{}/{}'.format(full_dir_path, _file)
    with open(file_path, 'r') as _in:
        for line in _in:
            report_string += line

    report_string += underscore

with open('{}/goal_report.txt'.format(personal_dir),'w') as _out:
    _out.write(report_string)

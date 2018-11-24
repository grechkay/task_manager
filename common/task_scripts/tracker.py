from taskw import TaskWarrior
from datetime import datetime as dt
import sys
import matplotlib.pyplot as plt


now = dt.now().timestamp()
war = TaskWarrior()
tasks = war.load_tasks()
week = 7 * 24 * 60 * 60
month = 4 * week

if len(sys.argv) > 1:
    plot_start = now - int(sys.argv[1])
else:
    plot_start = now - month

base_graphs = 0
num_graphs = 0
for task in tasks['pending']:
    annotations = task.get('annotations')
    min_freq = task.get('min_frequency')
    freq = task.get('weekly_frequency')
    tags = task.get('tags')

    if annotations is None or min_freq is None or freq is None:
        continue
    if 'numeric' in tags:
        num_graphs += 1
    else:
        base_graphs += 1

fig, ax = plt.subplots(2,max(base_graphs, num_graphs),dpi=300, figsize=(10,10))

_base_graphs = 0
_num_graphs = 0

for task in tasks['pending']:
    annotations = task.get('annotations')
    min_freq = task.get('min_frequency')
    freq = task.get('weekly_frequency')
    tags = task.get('tags')

    if annotations is None or min_freq is None or freq is None:
        continue
    min_freq = int(min_freq)
    freq = int(freq)
    
    if 'numeric' in tags:
        time_list = []
        value_list = []
    entries = 0
    for entry in annotations:
#        entries = 0
        dt_object = dt.strptime(entry['entry'], '%Y%m%dT%H%M%S%z')
        ts = dt_object.timestamp()

#        if now - ts < week:
#            entries += 1

        if 'numeric' in tags and ts > plot_start:
            time_list.append(ts)
            value_list.append(float(entry['description']))
        elif now - ts < week:
            entries += 1
    
    if 'numeric' in tags:
        ax[1][_num_graphs].set_title(task['description'])
        ax[1][_num_graphs].plot(time_list, value_list)
        ax[1][_num_graphs].scatter(time_list, value_list)
        _num_graphs += 1
    else:
        ax[0][_base_graphs].set_title(task['description'])
        ax[0][_base_graphs].axhline(y=0, linewidth=8, color='r')
        ax[0][_base_graphs].axhline(y=min_freq, linewidth=8, color='yellow')
        ax[0][_base_graphs].axhline(y=freq, linewidth=8, color='green')
        ax[0][_base_graphs].axhline(y=entries, linewidth=4, color='blue')
#        print(entries)
        _base_graphs += 1 
        
#    print(task.get('description'), entries, min_freq, freq)

#print(time_list)
#print(value_list)
plt.show()
    

import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap
from datetime import timedelta
import numpy as np
# First argument is the project

current_dir = os.getcwd()
home_dir = str(Path.home())

if current_dir != '{}/core'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core')

all_track_targets = os.listdir('personal/track_targets')

cmap_dict = {
    'up': 'RdYlGn',
    'down': 'RdYlGn_r'
}

def get_color_map(original):
    default = cm.get_cmap(original, 256)
    newcolors = default(np.linspace(0, 1, 256))
    black = np.array([0,0,0,1])
    newcolors[:1,:] = black
    newcmp = ListedColormap(newcolors)
    return newcmp
    

titles = []
dfs = []
_range = []
cmaps = []
aggregators = []

today = datetime.now().date()
day_delta = timedelta(days=1)
days_offset = 0
temp_day = today - day_delta * days_offset

while temp_day.strftime('%a') != 'Mon':
    days_offset += 1
    temp_day = today - day_delta * days_offset

days_offset += 7 * (int(sys.argv[1]) - 1)
first_day = (today - days_offset * day_delta).strftime('%Y-%m-%d')
day_to_idx = {}
for i in range(days_offset+1):
    date_str = (today - day_delta * i).strftime('%Y-%m-%d')
    day_to_idx[date_str] = days_offset  - i

for track_target in all_track_targets:
    title = track_target.split('.')[0]
    df = pd.read_csv(
        'personal/track_targets/{}'.format(track_target),
        skiprows=1,
        header=None,
        index_col=0
    )
    df = df.loc[df.index >= first_day,:]
    if df.shape[0] > 0:
        titles.append(title)
        dfs.append(df)
        

        with open('personal/track_targets/{}'.format(track_target)) as f:
            first_line = f.readline()
        low, high, cmap_dir, aggregator = first_line.split(',')
        _range.append((float(low) - 0.1, float(high) + 0.1))
        cmaps.append(cmap_dict[cmap_dir.strip()])
        aggregators.append(aggregator.strip())

plt.style.use("dark_background")
x_tick_labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
fig = plt.figure(figsize=(30 ,5 * len(titles)))

for i in range(len(titles)):
    minrange = _range[i][0]
    maxrange = _range[i][1]
    _ax = fig.add_subplot(len(titles),4 , i + 1)

    _ax.get_yaxis().set_visible(False)
    _ax.set_title(titles[i], fontsize=20)
    _ax.set_xticklabels(x_tick_labels, ha='left')
    nrows = days_offset // 7 + 1

    status_array = [_range[i][0] - 0.2] * nrows * 7
    status_array = np.array(status_array).reshape(nrows, 7)

    data = dfs[i].groupby(by=lambda x:x).agg(aggregators[i])
    zipped_data = zip(data.index.values, data[1].values)
    
    for date, val in zipped_data:
        idx = day_to_idx[date]
        status_array[nrows - 1 - idx // 7, idx % 7] = val

    newcmp = get_color_map(cmaps[i])
    pcm = _ax.pcolormesh(
        status_array, 
        edgecolors='grey', 
        linewidths=4,
        cmap=newcmp,
        vmin=minrange, 
        vmax=maxrange
    )

    fig.colorbar(pcm, ax=_ax, orientation='horizontal',cmap=newcmp)

plt.tight_layout(pad=10, w_pad=10, h_pad=10)
plt.show()
fig.savefig('personal/status.png')

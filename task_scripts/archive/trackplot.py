import sys, tempfile, os
from subprocess import call
from taskw import TaskWarrior
from datetime import datetime
from pathlib import Path
import pandas as pd
import calmap
import matplotlib.pyplot as plt
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

titles = []
dfs = []
_range = []
cmaps = []
aggregators = []
year = int(datetime.now().year)

####
# This is a hack to get the timezone right.
# When I move to a new location, I need to modify this code with the
# right timezone.
timedelta = -pd.Timedelta('08:00:00')
####

for track_target in all_track_targets:
    title = track_target.split('.')[0]
    df = pd.read_csv(
        'personal/track_targets/{}'.format(track_target),
        skiprows=1,
        header=None,
        index_col=0
    )
    df.index = pd.to_datetime(df.index.values, unit='s') + timedelta
    has_year = False
    for dt in df.index.values:
        dt_year = dt.astype('datetime64[Y]').astype(int) + 1970
        if dt_year == year:
            has_year = True
            break
    if not has_year:
        continue
    titles.append(title)
    dfs.append(df)
        

    with open('personal/track_targets/{}'.format(track_target)) as f:
        first_line = f.readline()
    low, high, cmap_dir, aggregator = first_line.split(',')
    _range.append((float(low) - 0.1, float(high) + 0.1))
    cmaps.append(cmap_dict[cmap_dir.strip()])
    aggregators.append(aggregator.strip())

plt.style.use("dark_background")
fig = plt.figure(figsize=(15 * 3 ,3.5 * len(titles)))

for i in range(len(titles)):
    _ax = fig.add_subplot(6, 3, i + 1)
    if len(titles) > 100: 
        #This is does because of an apparent subplots inconsistency when 
        #the number of subplots is 1.
        _ax = ax[i]
    else:
        _ax = _ax
    try:
        cax = calmap.yearplot(
            dfs[i].iloc[:,0],
            year=year,
            how=aggregators[i],
            fillcolor='grey',
            linecolor='grey',
            vmin=_range[i][0],
            vmax=_range[i][1],
            ax=_ax,
            cmap=cmaps[i]
        )
        _ax.set_title(titles[i], fontsize=20)
        fig.colorbar(cax.get_children()[1], ax=cax, orientation='horizontal')
    except:
        pass
        


plt.show()
fig.savefig('personal/status.png')

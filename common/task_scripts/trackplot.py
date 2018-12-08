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

if current_dir != '{}/core/common'.format(home_dir):
    raise ValueError('Wrong directory; switch to ~/core/common')

all_track_targets = os.listdir('track_targets')

titles = []
dfs = []

for track_target in all_track_targets:
    title = track_target.split('.')[0]
    df = pd.read_csv(
        'track_targets/{}'.format(track_target),
        header=None,
        index_col=0
    )
    df.index = pd.to_datetime(df.index.values * 1000000000)

    titles.append(title)
    dfs.append(df)

if len(titles) == 1:
    calmap.calendarplot(dfs[0].iloc[:,0],fillcolor='lightblue', vmin=0, fig_kws=dict(figsize=(24, 3)))
    plt.title(titles[0], fontsize=40)
else:
    fig, ax = plt.subplots(nrows= len(titles), ncols=1, figsize = (24, 4 * len(titles)))

    for i in range(len(titles)):
        calmap.yearplot(dfs[i].iloc[:,0],fillcolor='lightblue', vmin=0, ax=ax[i])
        ax[i].set_title(titles[i], fontsize=40)

plt.show()

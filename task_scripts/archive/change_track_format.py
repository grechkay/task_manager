import pandas as pd
import os

files = os.listdir()
timedelta = -pd.Timedelta('08:00:00')
for _file in files:
    if _file[-2:] == 'py':
        continue
    df = pd.read_csv(_file, skiprows=1,header=None,index_col=0)
    df.index = pd.to_datetime(df.index.values, unit='s') + timedelta
    df.index = df.index.strftime('%Y-%m-%d')

    with open(_file) as f:
        first_line = f.readline()

    with open(_file,'w') as f:
        f.write(first_line)
        df.to_csv(f,header=False)


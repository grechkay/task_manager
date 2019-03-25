import os
import argparse
from tools import get_date_from_string, bcolors, raise_fail_error
from project_manager import ProjectManager
import pandas as pd
from datetime import datetime

def show_tracks_for_date(track_date, all_track_targets, track_targets_path):
    for t in all_track_targets:

        try: # try to read the csv file
            df = pd.read_csv(
                '{}/{}'.format(track_targets_path, t),
                skiprows=1,
                header=None,
                index_col=0
            )
            read_csv = True
        except:
            read_csv = False
            nb_tracked = 0
            print(bcolors.ENDC + bcolors.BOLD, end='')

        if read_csv:
            # count entries for date
            counts = df.groupby(0).aggregate('count')
            try:
                nb_tracked = counts.loc[track_date].values[0]
                print(bcolors.BOLD + bcolors.OKBLUE, end='')
            except KeyError:
                nb_tracked = 0
                print(bcolors.ENDC + bcolors.BOLD, end='')

        # get first line to see the min, max values
        with open('{}/{}'.format(track_targets_path, t)) as f:
            first_line = f.readline()
        low, high, cmap_dir, aggregator, unit = first_line.split(',')
        text = str(nb_tracked) + bcolors.ENDC + " (" + low + "," + high + ")"

        print('\t' + t[: -len('.track')] + ' : \t' + text + bcolors.ENDC)  # so that the '.track' doesn't appear
    print()

def main(track_date, track_target, track_value):
    pm = ProjectManager()
    track_path = pm.personal_dir
    track_targets_path = '{}/track_targets'.format(track_path)
    all_track_targets = os.listdir(track_targets_path)

     # today
    if not track_target and not track_date and not track_value: # user just called track.py with no arguments --> show targets for today
        print("\nCurrent track targets for today :")
        today = datetime.now().strftime('%Y-%m-%d')
        show_tracks_for_date(today, all_track_targets, track_targets_path)
        return
    elif track_date and not track_target and not track_value: # user provided a date but nothing else
        # let's see if track_target is actually the date!
        track_date, dt = get_date_from_string(track_date)
        print("\nCurrent track targets for {}".format(track_date))
        show_tracks_for_date(track_date, all_track_targets, track_targets_path)
        return
    elif not track_target or not track_date or not track_value: # user forgot 1 argument
        raise_fail_error("Error. please execute \n\tpython goals.py [target] [YYYY-MM-DD] [value]")

    track_date, dt = get_date_from_string(track_date)

    if '{}.track'.format(track_target) not in all_track_targets:
        raise_fail_error("Error. Target is not tracked.")

    with open('{}/track_targets/{}.track'.format(track_path, track_target), 'a') as _in:
        _in.write('{ds},{val}\n'.format(ds=track_date, val=track_value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog="To view the targets you currently have, call this function without arguments.\n\n")
    parser.add_argument('date', type=str, nargs='?', help='possible values: [t, y, tom, YYYY-MM-DD] (for today, yesterday, tomorrow or a precise date)')
    parser.add_argument('target_name', type=str,  nargs='?', help='name of target to track')
    parser.add_argument('value', type=str, nargs='?', help='value given to the target.')
    args = parser.parse_args()
    main(args.date, args.target_name, args.value)


import os
import argparse
from tools import get_date_from_string, bcolors, raise_fail_error
from project_manager import ProjectManager

def main(track_target, track_date, track_value):
    pm = ProjectManager()
    track_path = pm.personal_dir
    all_track_targets = os.listdir('{}/track_targets'.format(track_path))

    if not track_target and not track_date and not track_value:
        print("\nCurrent track targets:")
        for t in all_track_targets:
            print(bcolors.BOLD + bcolors.OKBLUE + '\t' + t[: -len('.track')] + bcolors.ENDC)  # so that the '.track' doesn't appear
        print()
        return
    elif not track_target or not track_date or not track_value:
        raise_fail_error("Error. please execute \n\tpython goals.py [target] [YYYY-MM-DD] [value]")

    track_date, dt = get_date_from_string(track_date)

    if '{}.track'.format(track_target) not in all_track_targets:
        raise_fail_error("Error. Target is not tracked.")

    with open('{}/track_targets/{}.track'.format(track_path, track_target), 'a') as _in:
        _in.write('{ds},{val}\n'.format(ds=track_date, val=track_value))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(epilog="To view the targets you currently have, call this function without arguments.\n\n")
    parser.add_argument('target_name', type=str,  nargs='?', help='name of target to track')
    parser.add_argument('date', type=str, nargs='?', help='possible values: [t, y, tom, YYYY-MM-DD] (for today, yesterday, tomorrow or a precise date)')
    parser.add_argument('value', type=str, nargs='?', help='value given to the target.')
    args = parser.parse_args()
    main(args.target_name, args.date, args.value)


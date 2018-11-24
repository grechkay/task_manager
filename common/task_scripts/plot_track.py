from taskw import TaskWarrior
from datetime import datetime as dt

now = dt.now().timestamp()
war = TaskWarrior()
tasks = war.load_tasks()
week = 7 * 24 * 60 * 60

for task in tasks['pending']:
    annotations = task.get('annotations')
    min_freq = task.get('min_frequency')
    freq = task.get('weekly_frequency')
    if annotations is None or min_freq is None or freq is None:
        continue
    min_freq = int(min_freq)
    freq = int(freq)
    
    for entry in annotations:
        entries = 0
        dt_object = dt.strptime(entry['entry'], '%Y%m%dT%H%M%S%z')
        ts = dt_object.timestamp()

        if now - ts < week:
            entries += 1

    print(task.get('description'), entries, min_freq, freq)
    

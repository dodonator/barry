import json
from pathlib import Path

import pendulum

from entry import Entry
from workday import WorkDay


data_folder: Path = Path(__file__).parent / "data"
long_term_storage: Path = data_folder / "store.csv"
short_term_storage: Path = data_folder / "short.json"

# create data folder if missing
if not data_folder.exists():
    data_folder.mkdir()

# load current entry from short term memory
wd: WorkDay
if short_term_storage.exists():
    json_data = json.loads(short_term_storage.read_text())
    wd = WorkDay.from_dict(json_data)
else:
    wd = WorkDay()

# create entry based on user input
wd_date: pendulum.Date
wd_date_str: str = input("Please enter the date for the entry: ")
if not wd_date_str:
    wd_date = pendulum.today("local")
else:
    wd_date = pendulum.parse(wd_date_str, strict=False)

wd_time: pendulum.Time
wd_time_str: str = input("Please enter the time for the entry: ")
if not wd_time_str:
    wd_time = pendulum.now("local").time()
else:
    wd_time = pendulum.parse(wd_time_str, strict=False).time()

entry_datetime = pendulum.datetime(
    wd_date.year,
    wd_date.month,
    wd_date.day,
    wd_time.hour,
    wd_time.minute,
    tz="local",
)

print("Please select which time you want to enter: ")

idx: int
entry_type: str
for idx, entry_key in enumerate(Entry.TYPES):
    print(idx, entry_key)

choice = input("> ")
entry_type: str = Entry.TYPES[int(choice)]

comment: str = input("Comment for this entry: ")

entry: Entry = Entry(entry_datetime, entry_type, comment)

wd.add_entry(entry)

with short_term_storage.open("w") as file:
    json_data = wd.to_dict()
    json.dump(json_data, file, indent=4)

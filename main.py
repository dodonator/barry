from pathlib import Path

import pendulum

from entry import Entry, ENTRY_FIELDS

data_folder: Path = Path(__file__).parent / "data"
long_term_storage: Path = data_folder / "store.csv"
short_term_storage: Path = data_folder / "short.json"

# create data folder if missing
if not data_folder.exists():
    data_folder.mkdir()

# load current entry from short term memory
entry: Entry
if short_term_storage.exists():
    json_text: str = short_term_storage.read_text()
    entry = Entry.loads(json_text)
else:
    entry = Entry()

# user input
entry_date: pendulum.Date
entry_date_str: str = input("Please enter the date for the entry: ")
if not entry_date_str:
    entry_date = pendulum.today("local")
else:
    entry_date = pendulum.parse(entry_date_str, strict=False)

entry_time: pendulum.Time
entry_time_str: str = input("Please enter the time for the entry: ")
if not entry_time_str:
    entry_time = pendulum.now("local").time()
else:
    entry_time = pendulum.parse(entry_time_str, strict=False).time()

entry_datetime = pendulum.datetime(
    entry_date.year,
    entry_date.month,
    entry_date.day,
    entry_time.hour,
    entry_time.minute,
    tz="local",
)

print("Please select which time you want to enter: ")

idx: int
entry_type: str
for idx in ENTRY_FIELDS:
    entry_key = ENTRY_FIELDS[idx]["key"]
    print(idx, entry_key)

choice = input("> ")
entry.set(int(choice), entry_datetime)

with short_term_storage.open("w") as file:
    file.write(entry.dumps())

import csv
from datetime import date, datetime
from pathlib import Path

FILENAME: str = "data.csv"
FIELDNAMES: tuple[str, ...] = ("datetime", "type")

folder: Path = Path(__file__).parent
store: Path = folder / FILENAME

# read from csv file
if store.exists():
    data: list[dict] = []
    with store.open() as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
else:
    data: list[dict] = []

# read entry date from user
e_day_str: str = input("Enter the day (leave blank for today) [dd.mm.yyyy]: ")
if not e_day_str:
    e_day: date = date.today()
else:
    e_day: date = datetime.strptime(e_day_str, "%d.%m.%Y").date()

# read entry time from user
e_time_str: str = input("Enter time (leave blank for now) [hh:mm]: ")
if not e_time_str:
    e_time: datetime = datetime.now()
else:
    e_time = datetime.strptime(e_time_str, "%H:%M")

# read type of entry
entry_types: tuple[str, ...] = (
    "start of work",
    "end of work",
    "start of break",
    "end of break",
)
idx: int
entry_type: str
for idx, entry_type in enumerate(entry_types):
    print(f"{idx}: {entry_type}")

entry_type: int = int(input("Type of entry: "))

data.append({"datetime": e_time.isoformat(), "type": entry_type})

# save entry to file
with store.open("w") as file:
    writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
    for row in data:
        writer.writerow(row)

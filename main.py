import csv
from datetime import datetime
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

# read time from user
entry: str = input("Enter time (hh:mm): ")
if not entry:
    entry_dt: datetime = datetime.now()
else:
    entry_dt = datetime.strptime(entry, "%H:%M")

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

data.append({"datetime": entry_dt.isoformat(), "type": entry_type})

# save entry to file
with store.open("w") as file:
    writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
    for row in data:
        writer.writerow(row)

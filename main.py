import csv
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

FILENAME: str = "data.csv"
FIELDNAMES: tuple[str, ...] = ("datetime", "type")

folder: Path = Path(__file__).parent
store: Path = folder / FILENAME


def read_csv(path: Path) -> list[dict]:
    """Reads csv data from file and returns list of dicts."""
    if path.exists():
        data: list[dict] = []
        with path.open() as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
    else:
        data: list[dict] = []
    return data


def write_csv(path: Path, data: Iterable[dict]):
    """Writes list of dicts to csv file."""
    with path.open("w") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        for row in data:
            writer.writerow(row)


def main():
    # read data from file
    current_data: list[dict] = read_csv(store)

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

    # write data to file
    current_data.append({"datetime": e_time.isoformat(), "type": entry_type})
    write_csv(store, current_data)


if __name__ == "__main__":
    main()

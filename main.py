import csv
from pathlib import Path
from typing import Iterable
import pendulum

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
    e_day_str: str = input("Enter the day (leave blank for today): ")
    e_day: pendulum.Date
    if not e_day_str:
        e_day = pendulum.today("local").date()
    else:
        e_day = pendulum.parse(e_day_str, strict=False).date()

    # read entry time from user
    e_time_str: str = input("Enter time (leave blank for now) [hh:mm]: ")
    e_time: pendulum.Time
    if not e_time_str:
        e_time = pendulum.now().time()
    else:
        e_time = pendulum.parse(e_time_str, strict=False).time()

    e_datetime: pendulum.DateTime = pendulum.datetime(
        year=e_day.year,
        month=e_day.month,
        day=e_day.day,
        hour=e_time.hour,
        minute=e_time.minute,
    )

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
    current_data.append({"datetime": e_datetime.isoformat(), "type": entry_type})
    write_csv(store, current_data)


if __name__ == "__main__":
    main()

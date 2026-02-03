import json
from pathlib import Path

import pendulum
from pendulum import Date, Time, DateTime

from entry import Entry
from workday import WorkDay

data_folder: Path = Path(__file__).parent / "data"
long_term_storage: Path = data_folder / "store.csv"
short_term_storage: Path = data_folder / "short.json"


def ask_for_entry() -> Entry:
    """Creates a entry object based on user input."""
    # ask for the date
    e_date_str: str = input("Please enter the date for the entry: ")
    e_date: Date
    if not e_date_str:
        # in case of empty input use today
        e_date = pendulum.today("local")
    else:
        e_date = pendulum.parse(e_date_str, strict=False)

    e_time_str: str = input("Please enter the time for the entry: ")
    e_time: Time
    if not e_time_str:
        e_time = pendulum.now("local").time()
    else:
        e_time = pendulum.parse(e_time_str, strict=False).time()

    entry_dt: DateTime = pendulum.datetime(
        e_date.year, e_date.month, e_date.day, e_time.hour, e_time.minute, tz="local"
    )

    # ask for entry type
    for idx, entry_key in enumerate(Entry.TYPES):
        print(idx, entry_key)

    type_choice: str = input("Please enter the type of the entry: ")
    if not type_choice.isdigit():
        raise ValueError(f"Invalid entry type: {type_choice}")
    if int(type_choice) not in range(len(Entry.TYPES)):
        raise ValueError(f"Invalid entry type: {type_choice}")
    entry_type: str = Entry.TYPES[int(type_choice)]

    # ask for comment
    comment: str = input("Comment for entry: ")

    entry: Entry = Entry(entry_dt, entry_type, comment)
    return entry


def main() -> None:
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

    user_entry = ask_for_entry()

    wd.add_entry(user_entry)

    with short_term_storage.open("w") as file:
        json_data = wd.to_dict()
        json.dump(json_data, file, indent=4)


if __name__ == "__main__":
    main()

import json
import uuid
from typing import Optional

from pendulum import DateTime, Duration


class Entry:
    entry_id: uuid.UUID
    work_start: DateTime
    work_end: DateTime
    break_start: DateTime
    break_end: DateTime

    def __init__(
        self,
        work_start: Optional[DateTime],
        work_end: Optional[DateTime],
        break_start: Optional[DateTime],
        break_end: Optional[DateTime],
        comment: Optional[str] = None,
    ):
        # create uuid
        self.entry_id = uuid.uuid4()

        self.work_start = work_start
        self.work_end = work_end
        self.break_start = break_start
        self.break_end = break_end
        self.comment = comment

    def total_duration(self) -> Duration | None:
        """Returns the total time, disregarding the break.

        Returns None if times are undefined.
        """
        if self.work_start is None or self.work_end is None:
            return None
        return self.work_end - self.work_start

    def break_duration(self) -> Duration | None:
        """Returns the break time of the entry.

        Returns None if times are undefined.
        """
        if self.break_start is None or self.break_end is None:
            return None

        return self.break_end - self.break_start

    def work_duration(self) -> Duration | None:
        """Returns the actual work time.

        Deducts the break from the total time.
        Returns None if times are undefined.
        """
        total_time = self.total_duration()
        if total_time is None:
            return None

        break_time: Duration | None = self.break_duration()
        if break_time is None:
            return None

        return total_time - break_time

    def is_finished(self) -> bool:
        """Returns True if the entry contains all mandatory times.

        Work start time and work end time are always required.
        Break start time is required, if a break end time is provided.
        Break end time is required, if a break start time is provided.
        Comments are always optional.
        """
        if self.work_start is None or self.work_end is None:
            return False

        if self.break_start is None and self.break_end is None:
            return True

        return False

    def dumps(self) -> str:
        """Returns JSON data of the entry as a string."""

        json_data = {
            "entry_id": str(self.entry_id),
            "work_start": self.work_start.isoformat(),
            "work_end": self.work_end.isoformat(),
            "break_start": self.break_start.isoformat(),
            "break_end": self.break_end.isoformat(),
            "comment": self.comment,
        }
        return json.dumps(json_data, indent=4)

    @staticmethod
    def loads(json_str: str) -> Entry:
        """Loads Entry from JSON data."""
        json_data = json.loads(json_str)
        entry = Entry(
            work_start=DateTime.fromisoformat(json_data["work_start"]),
            work_end=DateTime.fromisoformat(json_data["work_end"]),
            break_start=DateTime.fromisoformat(json_data["break_start"]),
            break_end=DateTime.fromisoformat(json_data["break_end"]),
            comment=json_data["comment"],
        )
        entry.entry_id = uuid.UUID(json_data["entry_id"])
        return entry

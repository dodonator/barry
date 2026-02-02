import json
import uuid
from typing import Optional

from pendulum import DateTime, Duration


class Entry:
    entry_id: uuid.UUID
    work_start: DateTime | None
    work_end: DateTime | None
    break_start: DateTime | None
    break_end: DateTime | None
    comment: str | None

    def __init__(
        self,
        work_start: Optional[DateTime] = None,
        work_end: Optional[DateTime] = None,
        break_start: Optional[DateTime] = None,
        break_end: Optional[DateTime] = None,
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

    def set(self, field: int, value: DateTime) -> None:
        """Sets entry field to given value.

        Dependencies for field must be fulfilled."""
        match field:
            case 0:
                self._set_work_start(value)
            case 1:
                self._set_work_end(value)
            case 2:
                self._set_break_start(value)
            case 3:
                self._set_break_end(value)
            case _:
                return

    def _set_work_start(self, dt: DateTime) -> None:
        if self.work_end is not None:
            assert dt < self.work_end, "work start must happen before the work end"
        self.work_start = dt

    def _set_work_end(self, dt: DateTime) -> None:
        assert self.work_start is not None, "don't set end of work, if start is missing"
        assert dt > self.work_start, "work end must happen after the work start"
        self.work_end = dt

    def _set_break_start(self, dt: DateTime) -> None:
        assert self.work_start is not None, (
            "before any break there has to be a work start"
        )
        assert dt > self.work_start, "break must happen after the work start"
        if self.work_end is not None:
            assert dt < self.work_end, "break must be started before the work end"

        self.break_start = dt

    def _set_break_end(self, dt: DateTime) -> None:
        assert self.work_start is not None and self.break_start is not None, (
            "don't set end of break, without start of work / break"
        )
        assert dt > self.break_start, "end of break must happen after start of break"

        if self.work_end is not None:
            assert dt < self.work_end, "break must be finished before work end"

        self.break_end = dt

    def dumps(self) -> str:
        """Returns JSON data of the entry as a string."""
        json_data = {
            "entry_id": str(self.entry_id),
            "work_start": self.work_start.isoformat()
            if self.work_start is not None
            else None,
            "work_end": self.work_end.isoformat()
            if self.work_end is not None
            else None,
            "break_start": self.break_start.isoformat()
            if self.break_start is not None
            else None,
            "break_end": self.break_end.isoformat()
            if self.break_end is not None
            else None,
            "comment": self.comment if self.comment is not None else None,
        }
        return json.dumps(json_data, indent=4)

    @staticmethod
    def loads(json_str: str) -> Entry:
        """Loads Entry from JSON data."""
        json_data = json.loads(json_str)
        work_start = json_data["work_start"]
        work_end = json_data["work_end"]
        break_start = json_data["break_start"]
        break_end = json_data["break_end"]
        comment = json_data.get("comment")

        entry = Entry(
            work_start=DateTime.fromisoformat(work_start)
            if work_start is not None
            else None,
            work_end=DateTime.fromisoformat(work_end) if work_end is not None else None,
            break_start=DateTime.fromisoformat(break_start)
            if break_start is not None
            else None,
            break_end=DateTime.fromisoformat(break_end)
            if break_end is not None
            else None,
            comment=comment,
        )
        entry.entry_id = uuid.UUID(json_data["entry_id"])
        return entry

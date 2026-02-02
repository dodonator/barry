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

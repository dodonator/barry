import uuid
from typing import Optional

import pendulum
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

    def worktime(self) -> Duration:
        """Returns the work time of the entry.

        Deducts the break from the work time.
        """
        if self.work_start is None or self.work_end is None:
            return pendulum.duration(0)

        work_time: pendulum.Duration = self.work_end - self.work_start
        if self.break_start is None or self.break_end is None:
            return work_time

        break_time: pendulum.Duration = self.break_end - self.break_start
        return work_time - break_time

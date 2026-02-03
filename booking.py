import pendulum
from pendulum import Date, Duration

from workday import WorkDay


class Booking:
    OVERTIME_THRESHOLD: Duration = pendulum.duration(hours=8)

    date: Date
    total: Duration
    work: Duration
    breaks: Duration
    balance: Duration

    def __init__(self, date: Date, total: Duration, work: Duration, breaks: Duration):
        self.date = date
        assert total == work + breaks
        self.total = total
        self.work = work
        self.breaks = breaks
        self.balance = work - self.OVERTIME_THRESHOLD

    def has_overtime(self) -> bool:
        """Returns whether this booking has overtime."""
        return self.work > self.OVERTIME_THRESHOLD

    def has_undertime(self) -> bool:
        """Returns whether this booking is below time requirement."""
        return self.work < self.OVERTIME_THRESHOLD

    @staticmethod
    def from_workday(wd: WorkDay) -> Booking:
        if not wd.is_valid():
            raise Exception("Workday has to be valid.")

        booking: Booking = Booking(
            date=wd.date,
            total=wd.total_time(),
            work=wd.work_time(),
            breaks=wd.break_time(),
        )
        return booking

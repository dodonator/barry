from pendulum import Date, Duration

from workday import WorkDay


class Booking:
    date: Date
    total: Duration
    work: Duration
    breaks: Duration

    def __init__(self, date: Date, total: Duration, work: Duration, breaks: Duration):
        self.date = date
        assert total == work + breaks
        self.total = total
        self.work = work
        self.breaks = breaks

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

from typing import Optional

from pendulum import Date, DateTime, Duration

from entry import Entry


class WorkDay:
    """A WorkDay contains the time data for the work time and the breaks during one workday."""

    date: Date
    entries: list[Entry]
    state: str

    def __init__(
        self,
        date: Optional[Date] = None,
    ):
        self.date = date
        self.entries = []
        self.state = "before_work"
        # Possible states: before_work, during_work, during_break, after_work

    def add_entry(self, entry: Entry):
        match entry.entry_type:
            case "work_start":
                self._set_work_start(entry)
            case "work_end":
                self._set_work_end(entry)
            case "break_start":
                self._set_break_start(entry)
            case "break_end":
                self._set_break_end(entry)
            case _:
                return

        # Sort the entries chronological
        self.entries.sort(key=lambda entry: entry.dt)

    def _set_work_start(self, entry: Entry):
        if self.state != "before_work":
            return
        self.entries.insert(0, entry)
        self.state = "during_work"

    def _set_work_end(self, entry: Entry):
        if self.state != "during_work":
            return
        self.entries.insert(-1, entry)
        self.state = "after_work"

    def _set_break_start(self, entry: Entry):
        if self.state != "during_work":
            return
        self.entries.append(entry)
        self.state = "during_break"

    def _set_break_end(self, entry: Entry):
        if self.state != "during_break":
            return
        self.entries.append(entry)
        self.state = "during_work"

    def is_valid(self):
        """Returns if the workday is valid.

        Each workday has to have:
        - exactly one entry defining the work start
        - exactly one entry defining the work end

        Additionally, each workday can have entries defining the breaks.
        For each break start, there has to be a corresponding entry defining the break end.
        """
        if self.entries[0].entry_type != "work_start":
            # return False if work start is missing
            return False
        if self.entries[-1].entry_type != "work_end":
            # return False if work end is missing
            return False

        on_break = False
        for entry in self.entries[1:-1]:
            if entry.entry_type == "break_start" and on_break:
                # return False if a break start is in the wrong place
                return False

            if entry.entry_type == "break_end" and not on_break:
                # return False if a break end is in the wrong place
                return False

            if entry.entry_type == "break_start":
                on_break = True

            if entry.entry_type == "break_end":
                on_break = False

        # return False if the state is not "after_work"
        if self.state != "after_work":
            return False

        return True

    def total_time(self) -> Duration:
        """Returns the total work time (including all breaks).

        WorkDay has to be valid.
        """
        if not self.is_valid():
            return Duration(0)
        start: DateTime = self.entries[0].dt
        end: DateTime = self.entries[-1].dt
        return end - start

    def break_time(self) -> Duration:
        """Sums up the break times."""
        break_duration: Duration = Duration(0)
        if not self.is_valid():
            return break_duration

        # if only work start and work end are set, break time will be zero
        if len(self.entries) == 2:
            return break_duration

        break_starts: list[DateTime] = [
            entry.dt for entry in self.entries if entry.entry_type == "break_start"
        ]
        break_ends: list[DateTime] = [
            entry.dt for entry in self.entries if entry.entry_type == "break_end"
        ]
        break_starts.sort(key=lambda entry: entry.dt)
        break_ends.sort(key=lambda entry: entry.dt)

        for break_start, break_end in zip(break_starts, break_ends):
            current_break: Duration = break_end - break_start
            break_duration += current_break

        return break_duration

import uuid

import pendulum


class Entry:
    WORK_START: str = "work_start"
    WORK_END: str = "work_end"
    BREAK_START: str = "break_start"
    BREAK_END: str = "break_end"

    TYPES: tuple[str, ...] = (WORK_START, WORK_END, BREAK_START, BREAK_END)

    entry_id: uuid.UUID
    entry_type: str
    dt: pendulum.DateTime
    comment: str

    def __init__(
        self, dt: pendulum.DateTime, entry_type: str, comment: str | None = None
    ) -> None:
        self.entry_id = uuid.uuid4()
        if entry_type not in self.TYPES:
            raise ValueError(f"Invalid entry type: {entry_type}")
        self.entry_type = entry_type
        self.dt = dt
        self.comment = comment

    def to_dict(self) -> dict[str, str]:
        """Returns entry as a dict."""
        return {
            "entry_id": str(self.entry_id),
            "entry_type": self.entry_type,
            "dt": self.dt.isoformat(),
            "comment": self.comment,
        }

    @staticmethod
    def from_dict(data: dict[str, str]) -> Entry:
        """Creates entry from a dict."""
        entry = Entry(
            entry_type=data["entry_type"],
            dt=pendulum.DateTime.fromisoformat(data["dt"]),
            comment=data["comment"],
        )
        entry.entry_id = uuid.UUID(data["entry_id"])
        return entry

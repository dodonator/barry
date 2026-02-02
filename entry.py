import uuid
import pendulum


class Entry:
    entry_id: uuid.UUID
    entry_type: str
    dt: pendulum.DateTime
    comment: str

    def __init__(
        self, dt: pendulum.DateTime, entry_type: str, comment: str | None = None
    ) -> None:
        self.entry_id = uuid.uuid4()
        self.entry_type = entry_type
        self.dt = dt
        self.comment = comment
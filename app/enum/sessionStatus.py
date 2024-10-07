from enum import Enum

class SessionStatus(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PAUSED = "paused"
from enum import Enum

# TODO this is too confusing and a bad pattern, I think it's even a tagged class anti-pattern so let's get rid of it
class SnapDirection(Enum):
    SENT = "SENT"
    RECEIVED = "RECEIVED"

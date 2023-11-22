from enum import Enum
import logging

# ENUMS MODELS #

class WorkSchedule(str, Enum):
    """Enum que representa las posibles jornadas de trabajo."""

    FULL_TIME = "FULL-TIME"
    PART_TIME = "PART-TIME"
    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"
    DAY = "DAY"
    NIGHT = "NIGHT"
    FLEXTIME = "FLEXTIME"
    REMOTE_WORK = "REMOTE-WORK"
    ANY = "ANY"

class UserType(str, Enum):
    """Enum que representa los tipos de usuario."""

    CANDIDATE = "CANDIDATE"
    COMPANY = "COMPANY"
    ADMIN = "ADMIN"


# ENUMS UTILS #

class LogLevel(Enum):
    """Enum que representa los niveles de log."""

    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

from dataclasses import dataclass


@dataclass
class LogLineDto:
    row_line: str
    unix_time: int

from dataclasses import dataclass


@dataclass
class LogLineDto:
    remotehost: str
    rfc931: str
    authuser: str
    date: float
    request: str
    status: int
    bytes: float

    @property
    def unix_time(self) -> int:
        return int(self.date)

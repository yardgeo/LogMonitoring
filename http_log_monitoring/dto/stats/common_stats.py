from dataclasses import dataclass, field

from .bytes_stats import BytesStatsDto
from .request_stats import RequestStatsDto
from .status_stats import StatusStatsDto


@dataclass
class CommonStatsDto:
    """
    A class to represent common statistics of logs
    """

    bytes_stats_dto: BytesStatsDto = field(default_factory=BytesStatsDto)
    status_stats_dto: StatusStatsDto = field(default_factory=StatusStatsDto)
    request_stats_dto: RequestStatsDto = field(default_factory=RequestStatsDto)

    def __str__(self):
        return f"Requests statistic:\n{str(self.request_stats_dto)}\n" \
               f"---------------------------------------------------\n" \
               f"Response status statistic:\n{str(self.status_stats_dto)}\n" \
               f"---------------------------------------------------\n" \
               f"Bytes statistic:\n{str(self.bytes_stats_dto)}\n" \
               f"---------------------------------------------------"

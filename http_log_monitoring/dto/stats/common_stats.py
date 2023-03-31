from abc import ABC
from dataclasses import dataclass

from .bytes_stats import BytesStatsDto
from .status_stats import StatusStatsDto
from .request_stats import RequestStatsDto


@dataclass
class CommonStatsDto(ABC):
    bytes_stats_dto: BytesStatsDto = BytesStatsDto()
    status_stats_dto: StatusStatsDto = StatusStatsDto()
    request_stats_dto: RequestStatsDto = RequestStatsDto()

    def __str__(self):
        return f"Requests statistic:\n{str(self.request_stats_dto)}\n" \
               f"---------------------------------------------------\n" \
               f"Response status statistic:\n{str(self.status_stats_dto)}\n" \
               f"---------------------------------------------------\n" \
               f"Bytes statistic:\n{str(self.bytes_stats_dto)}\n" \
               f"---------------------------------------------------"

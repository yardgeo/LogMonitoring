from dto import CommonStatsDto, LogLineDto


class TrafficStatsHandlerState:

    def __init__(self):
        self._common_stats = CommonStatsDto()

    def clear(self) -> None:
        self._common_stats = CommonStatsDto()

    def update(self, log_line: LogLineDto) -> None:
        self._update_bytes_stats(log_line.bytes)
        self._update_status_stats(log_line.status)
        self._update_request_stats(log_line.request)

    def get_notification_message(self) -> str:
        return str(self._common_stats)

    def _update_bytes_stats(self, bytes_v: float) -> None:
        self._common_stats.bytes_stats_dto.max_bytes = max(self._common_stats.bytes_stats_dto.max_bytes, bytes_v)
        self._common_stats.bytes_stats_dto.sum_bytes += bytes_v

    def _update_status_stats(self, status: int) -> None:
        if status // 100 == 2:
            self._common_stats.status_stats_dto.number_2xx += 1
        elif status // 100 == 4:
            self._common_stats.status_stats_dto.number_4xx += 1
        elif status // 100 == 5:
            self._common_stats.status_stats_dto.number_5xx += 1
        else:
            self._common_stats.status_stats_dto.number_others += 1

    def _update_request_stats(self, request: str) -> None:
        # TODO exceptions handler
        method, url, protocol = request.split()
        self._common_stats.request_stats_dto.method_count_dict[method] += 1
        self._common_stats.request_stats_dto.section_count_dict[url.split("/")[1]] += 1

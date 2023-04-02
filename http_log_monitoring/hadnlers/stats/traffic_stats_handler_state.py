from dto import CommonStatsDto, LogLineDto
from utils import reset_all_to_defaults


class TrafficStatsHandlerState:
    """
    A class to represent a state for traffic stats handler
    """

    def __init__(self):
        self._common_stats = CommonStatsDto()

    def clear(self) -> None:
        """
        Clear state as time interval of interest is ended.
        """
        reset_all_to_defaults(self._common_stats)

    def update(self, log_line: LogLineDto) -> None:
        """
        Update state with new log line information
        :param log_line: line of log
        :type log_line: LogLineDto
        """
        # update stats for request bytes
        self._update_bytes_stats(log_line.bytes)

        # update stats for request status code
        self._update_status_stats(log_line.status_code)

        # update stats for request info
        self._update_request_stats(method=log_line.http_method, section=log_line.web_site_section)

    def get_notification_message(self) -> str:
        """
        Create statistics notification message based on current state
        :return: Notification message
        :rtype: str
        """
        return str(self._common_stats)

    def _update_bytes_stats(self, bytes_v: float) -> None:
        # update maximum
        self._common_stats.bytes_stats_dto.max_bytes = max(self._common_stats.bytes_stats_dto.max_bytes, bytes_v)

        # update sum
        self._common_stats.bytes_stats_dto.sum_bytes += bytes_v

    def _update_status_stats(self, status_code: int) -> None:
        # increase counter for code
        if status_code // 100 == 2:
            self._common_stats.status_stats_dto.number_2xx += 1
        elif status_code // 100 == 4:
            self._common_stats.status_stats_dto.number_4xx += 1
        elif status_code // 100 == 5:
            self._common_stats.status_stats_dto.number_5xx += 1
        else:
            self._common_stats.status_stats_dto.number_others += 1

    def _update_request_stats(self, method: str, section: str) -> None:
        # increase counter for method
        self._common_stats.request_stats_dto.method_count_dict[method] += 1

        # increase counter for section
        self._common_stats.request_stats_dto.section_count_dict[section] += 1

from unittest import TestCase

from dto import LogLineDto
from hadnlers.stats import TrafficStatsHandlerState
from .test_utils import dataclass_equal_to_defaults


class TestTrafficStatsHandlerState(TestCase):
    def setUp(self) -> None:
        self._state = TrafficStatsHandlerState()
        self._state.clear()

    def tearDown(self) -> None:
        self._state.clear()

    def _update(self, log_line: LogLineDto):
        self._state.update(log_line)

    def test_clear(self):
        self.assertTrue(dataclass_equal_to_defaults(self._state._common_stats))
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 200.0,
                         'bytes': 1234.0}
        self._update(LogLineDto(**log_line_dict))
        self.assertFalse(
            dataclass_equal_to_defaults(self._state._common_stats))
        self._state.clear()
        self.assertTrue(dataclass_equal_to_defaults(self._state._common_stats))

    def test_update_http_code_2xx_status(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 200.0,
                         'bytes': 1234.0}
        self._update(LogLineDto(**log_line_dict))
        self.assertEqual(
            self._state._common_stats.status_stats_dto.number_2xx,
            1
        )
        self.assertEqual(
            self._state._common_stats.status_stats_dto.number_4xx,
            0
        )
        self.assertEqual(
            self._state._common_stats.status_stats_dto.number_5xx,
            0
        )
        self.assertEqual(
            self._state._common_stats.status_stats_dto.number_others,
            0
        )

    def test_update_http_code_1xx_status(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 1234.0}
        self._update(LogLineDto(**log_line_dict))

        self.assertEqual(
            self._state._common_stats.status_stats_dto.number_2xx,
            0
        )
        self.assertEqual(
            self._state._common_stats.status_stats_dto.number_4xx,
            0
        )
        self.assertEqual(
            self._state._common_stats.status_stats_dto.number_5xx,
            0
        )
        self.assertEqual(
            self._state._common_stats.status_stats_dto.number_others,
            1
        )

    def test_update_bytes_maxim(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 1234.0}
        self._update(LogLineDto(**log_line_dict))

        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 124.0}
        self._update(LogLineDto(**log_line_dict))

        self.assertEqual(
            self._state._common_stats.bytes_stats_dto.max_bytes,
            1234.0
        )

    def test_update_bytes_sum(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 1234.0}
        self._update(LogLineDto(**log_line_dict))
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 124.0}
        self._update(LogLineDto(**log_line_dict))

        self.assertEqual(
            self._state._common_stats.bytes_stats_dto.sum_bytes,
            1358.0
        )

    def test_update_request_method(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 1234.0}
        self._update(LogLineDto(**log_line_dict))
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 124.0}
        self._update(LogLineDto(**log_line_dict))
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'POST /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 124.0}
        self._update(LogLineDto(**log_line_dict))

        self.assertEqual(
            self._state._common_stats.request_stats_dto.method_count_dict[
                'GET'],
            2
        )
        self.assertEqual(
            self._state._common_stats.request_stats_dto.method_count_dict[
                'POST'],
            1
        )
        n = len(self._state._common_stats.request_stats_dto.method_count_dict)
        self.assertEqual(n, 2)

    def test_update_request_section(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 1234.0}
        self._update(LogLineDto(**log_line_dict))
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/model HTTP/1.0', 'status': 120.0,
                         'bytes': 124.0}
        self._update(LogLineDto(**log_line_dict))
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'POST /report HTTP/1.0', 'status': 120.0,
                         'bytes': 124.0}
        self._update(LogLineDto(**log_line_dict))

        self.assertEqual(
            self._state._common_stats.request_stats_dto.section_count_dict[
                'api'],
            2
        )
        self.assertEqual(
            self._state._common_stats.request_stats_dto.section_count_dict[
                'report'],
            1
        )
        n = len(self._state._common_stats.request_stats_dto.section_count_dict)
        self.assertEqual(n, 2)

    def test_get_notification_message(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 120.0,
                         'bytes': 1234.0}
        self._update(LogLineDto(**log_line_dict))
        self.assertIsInstance(self._state.get_notification_message(), str)
        self.assertGreater(len(self._state.get_notification_message()), 20)

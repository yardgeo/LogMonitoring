from unittest import TestCase

from dto import LogLineDto
from exceptions import LogLineParsingException


class TestLogLineDto(TestCase):
    def test_log_contains_wrong_format(self):
        log_line_dict = {'remotehost': '10.0.0.2', 'rfc931': '-',
                         'authuser': '', 'date': None, 'request': None,
                         'status': None, 'bytes': None}
        self.assertRaises(LogLineParsingException, LogLineDto, **log_line_dict)

    def test_log_contains_nones(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': '200',
                         'bytes': 1234.0}
        self.assertRaises(LogLineParsingException, LogLineDto, **log_line_dict)

    def test_log_request_no_spaces(self):
        # no spaces
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET/api/userHTTP/1.0', 'status': 200.0,
                         'bytes': 1234.0}
        self.assertRaises(LogLineParsingException, LogLineDto, **log_line_dict)

    def test_log_request_invalid_order(self):
        # invalid slashes
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': '/api/help GET HTTP/1.0', 'status': 200.0,
                         'bytes': 1234.0}
        self.assertRaises(LogLineParsingException, LogLineDto, **log_line_dict)

    def test_log_request_no_slashes(self):
        # no slashes
        log_line_dict = {'remotehost': '10.0.0.5', 'rfc931': '-',
                         'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET apihelp HTTP/1.0', 'status': 200.0,
                         'bytes': 1234.0}
        self.assertRaises(LogLineParsingException, LogLineDto, **log_line_dict)

import asyncio
from unittest import IsolatedAsyncioTestCase, TestCase
from unittest.mock import AsyncMock, MagicMock

from config import Config
from dto import LogLineDto
from dispatcher import Dispatcher


class TestDispatcher(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self._dispatcher = Dispatcher(log_file_path=Config.LOCAL_PRODUCER_FILEPATH)
        self._mock_handlers = []
        for handler in self._dispatcher._handlers:
            mock = AsyncMock()
            handler.handle = mock
            handler.start = AsyncMock()
            self._mock_handlers.append(mock)

    async def test_handle(self):
        log_line_dict = {'remotehost': '10.0.0.4', 'rfc931': '-', 'authuser': 'apache', 'date': 1549573860.0,
                         'request': 'GET /api/user HTTP/1.0', 'status': 200.0, 'bytes': 1234.0}
        n = 5
        log_line = LogLineDto(**log_line_dict)
        mock_stream_logs = MagicMock()
        mock_stream_logs.__aiter__.return_value = (log_line for _ in range(n))
        self._dispatcher._producer.stream_logs = lambda: mock_stream_logs
        task = asyncio.create_task(self._dispatcher._handle_logs())
        await asyncio.sleep(0)
        for mock_handler in self._mock_handlers:
            self.assertEqual(mock_handler.call_count, n)
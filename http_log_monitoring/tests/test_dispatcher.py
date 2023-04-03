import random
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock

from config import Config
from dispatcher import Dispatcher
from exceptions import LogLineStreamFinishedException
from .generators import generate_n_log_lines


class TestDispatcher(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        # create dispatcher instance
        self._dispatcher = Dispatcher(
            log_file_path=Config.LOCAL_PRODUCER_FILEPATH)

        # mock handle function for handlers
        self._mock_handlers = []
        for handler in self._dispatcher._handlers:
            mock = AsyncMock()
            handler.handle = mock
            handler.start = AsyncMock()
            self._mock_handlers.append(mock)

    async def test_handle(self):
        # mock log producer
        n = random.randrange(10)
        mock_stream_logs = MagicMock()
        mock_stream_logs.__aiter__.return_value = generate_n_log_lines(n)
        self._dispatcher._producer.stream_logs = lambda: mock_stream_logs

        # test that stream is finished
        with self.assertRaises(LogLineStreamFinishedException):
            await self._dispatcher._handle_logs()

        # test that for each handler all logs were handled
        for mock_handler in self._mock_handlers:
            self.assertEqual(mock_handler.call_count, n)

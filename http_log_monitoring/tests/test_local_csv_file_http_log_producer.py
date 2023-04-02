import asyncio
import csv
from unittest import IsolatedAsyncioTestCase

from config import Config
from dto import LogLineDto
from producers import LocalCSVFileHttpLogProducer


class TestLocalCSVFileHttpLogProducer(IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.file_path = Config.LOCAL_PRODUCER_FILEPATH
        self.producer = LocalCSVFileHttpLogProducer(self.file_path)

    async def test_start_is_doing_nothing(self):
        # get number of running tasks
        num_of_running_tasks = len(asyncio.all_tasks())

        # schedule the coroutine to run in the background
        asyncio.create_task(self.producer.start())

        # allow the task to run
        await asyncio.sleep(0)

        # check that number of running tasks wasn't changed
        self.assertEqual(len(asyncio.all_tasks()), num_of_running_tasks)


class TestOfflineFile(TestLocalCSVFileHttpLogProducer):

    async def test_log_stream_length_less_than_actual(self):
        # count actual length
        with open(self.file_path) as fin:
            actual_len = sum(1 for _ in fin)

        # subtract 1 because first line is header
        actual_len -= 1

        # count generated length
        generated_len = 0
        async for _ in self.producer.stream_logs():
            generated_len += 1
            if generated_len == actual_len:
                break
        self.assertEqual(generated_len, actual_len)

    async def test_log_stream_length_greater_than_actual(self):
        # count actual length
        with open(self.file_path) as fin:
            actual_len = sum(1 for _ in fin)

        # subtract 1 because first line is header
        actual_len -= 1

        # count generated length
        generated_len = 0
        gen = self.producer.stream_logs()
        async for _ in gen:
            generated_len += 1
            if generated_len == actual_len:
                break
        try:
            await asyncio.wait_for(
                gen.__aiter__().__anext__(),
                timeout=1)
            self.fail("There are some more elements in generator")
        except asyncio.TimeoutError:
            pass

    async def test_log_stream_elements_are_correct(self):
        # count actual length
        actual_logs = []
        with open(self.file_path) as fin:
            log_reader = csv.DictReader(fin,
                                        quoting=csv.QUOTE_NONNUMERIC)
            for line in log_reader:
                actual_logs.append(LogLineDto(**line))

        # count generated length
        i = 0
        async for log in self.producer.stream_logs():
            self.assertEqual(log, actual_logs[i])
            i += 1
            if i == len(actual_logs):
                break

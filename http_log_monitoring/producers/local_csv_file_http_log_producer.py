import asyncio
import csv
from typing import AsyncIterable

from config import Config
from dto import LogLineDto
from producers import HttpLogProducer


class LocalCSVFileHttpLogProducer(HttpLogProducer):
    def __init__(self,
                 file_path: str):
        self._file_path = file_path

    async def stream_logs(self) -> AsyncIterable[LogLineDto]:
        with open(self._file_path) as file:
            log_reader = csv.DictReader(file,
                                        delimiter=Config.LOCAL_PRODUCER_DELIMITER,
                                        quoting=csv.QUOTE_NONNUMERIC)
            while True:
                try:
                    raw_log_dict = next(log_reader)
                except StopIteration:
                    await asyncio.sleep(Config.LOCAL_PRODUCER_SLEEP_TIME)
                    continue
                yield LogLineDto(**raw_log_dict)

    async def start(self) -> None:
        pass  # Local file http log producer do not require additional process to start

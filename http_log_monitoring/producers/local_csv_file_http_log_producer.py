import asyncio
import csv
import logging
from typing import AsyncIterable

from config import Config
from dto import LogLineDto
from exceptions import LogLineParsingException
from producers import HttpLogProducer

# constants
QUEUE_MAX_SIZE = Config.LOCAL_PRODUCER_QUEUE_MAX_SIZE
ONLINE_SLEEP_TIME = Config.LOCAL_PRODUCER_ONLINE_SLEEP_TIME
DELIMITER = Config.LOCAL_PRODUCER_DELIMITER
FILEPATH = Config.LOCAL_PRODUCER_FILEPATH
OFFLINE_MODE = Config.LOCAL_PRODUCER_OFFLINE_MODE


class LocalCSVFileHttpLogProducer(HttpLogProducer):
    """
    A class to represent http log producer from a local csv file.
    """

    def __init__(self,
                 file_path: str):
        self._file_path = file_path
        self._logger = logging.getLogger()

    async def stream_logs(self) -> AsyncIterable[LogLineDto]:
        # open local file in read mode
        with open(self._file_path, "r") as file:
            # get csv reader witch convert line to {header: value} dict
            log_reader = csv.DictReader(file,
                                        delimiter=DELIMITER,
                                        quoting=csv.QUOTE_NONNUMERIC)

            # start infinite loop to read line by line in real time
            while True:
                # try to get new line
                try:
                    raw_log_dict = next(log_reader)

                # in case there are new log line
                except StopIteration:

                    # if offline mode stop stream
                    if OFFLINE_MODE:
                        break

                    # else sleep for LOCAL_PRODUCER_ONLINE_SLEEP_TIME
                    else:
                        await asyncio.sleep(ONLINE_SLEEP_TIME)
                        continue

                # yield next line
                try:
                    yield LogLineDto(**raw_log_dict)
                # catch parsing exceptions
                except LogLineParsingException as exp:
                    error_line = DELIMITER.join(
                        [str(v) for v in raw_log_dict.values()]
                    )
                    self._logger.error(
                        f"Parsing error for line {error_line}: {exp}")
                    continue

                # sleep 0 to handlers can proceed next line in background mode
                await asyncio.sleep(0)

    async def start(self) -> None:
        # Local file http log producer
        # do not require additional process to start
        pass

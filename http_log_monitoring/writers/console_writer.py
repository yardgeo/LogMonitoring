import logging
import sys
from asyncio import Queue

from writers import CommonWriter


class ConsoleWriter(CommonWriter):
    def __init__(self, message_queue: Queue):
        super().__init__(message_queue)
        self._logger = logging.getLogger()
        self._logger.addHandler(logging.StreamHandler(sys.stdout))

    async def write(self, msg: str) -> None:
        self._logger.info(msg)

    async def run(self) -> None:
        while True:
            msg = await self.message_queue.get()
            await self.write(msg)

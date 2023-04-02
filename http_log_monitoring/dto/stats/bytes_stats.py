from dataclasses import dataclass


@dataclass
class BytesStatsDto:
    """
    A class to represent statistics related to bytes information of logs
    """

    max_bytes: float = 0
    sum_bytes: float = 0

    def __str__(self):
        return f"Maximum bytes {self.max_bytes} and sum {self.sum_bytes}"

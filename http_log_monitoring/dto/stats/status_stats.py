from dataclasses import dataclass


@dataclass
class StatusStatsDto:
    number_4xx: int = 0
    number_5xx: int = 0
    number_2xx: int = 0
    number_others: int = 0

    def __str__(self):
        return f"Number of responses with status:\n" \
               f"2xx: {self.number_2xx} \n" \
               f"4xx: {self.number_4xx} \n" \
               f"5xx: {self.number_5xx} \n" \
               f"others: {self.number_others}"

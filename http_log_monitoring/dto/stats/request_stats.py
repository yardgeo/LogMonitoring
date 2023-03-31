from dataclasses import dataclass, field
from typing import Dict
from collections import defaultdict


@dataclass
class RequestStatsDto:
    section_count_dict: Dict[str, int] = field(default_factory=lambda: defaultdict(int))
    method_count_dict: Dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def __str__(self):
        section_count_str = "\n".join([f"{k}: {v}" for k, v in self.section_count_dict.items()])
        method_count_str = "\n".join([f"{k}: {v}" for k, v in self.method_count_dict.items()])
        return f"Statistic for HTTP methods (number of hits):\n" \
               f"{method_count_str}\n" \
               f"Statistic for web site sections (number of hits):\n" \
               f"{section_count_str}"

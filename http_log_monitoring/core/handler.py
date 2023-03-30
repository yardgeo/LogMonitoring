from writers import Writer
from readers import HttpLogReader


class Handler:
    def __init__(self,
                 alert_writer: Writer,
                 stats_writer: Writer,
                 http_log_reader: HttpLogReader):
        self._alert_writer = alert_writer
        self._stats_writer = stats_writer
        self._http_log_reader = http_log_reader

    def handle_stats(self):
        pass

    def handle_alerts(self):
        pass

    def run(self):
        pass

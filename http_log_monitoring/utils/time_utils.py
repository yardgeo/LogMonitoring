from datetime import datetime

from config import Config


def format_unix_time(unix_time: int) -> str:
    """
    format unix time date to string timestamp
    :param unix_time: unix time
    :type unix_time: int
    :return: formatted date
    :rtype: str
    """
    return datetime.utcfromtimestamp(unix_time).strftime(
        Config.DATETIME_FORMAT)

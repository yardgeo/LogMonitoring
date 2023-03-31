import os


class Config:
    # Common constants
    DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", '%Y-%m-%d %H:%M:%S')

    # Local producers constants
    LOCAL_PRODUCER_QUEUE_MAX_SIZE = os.getenv("LOCAL_PRODUCER_QUEUE_MAX_SIZE", 20)
    LOCAL_PRODUCER_SLEEP_TIME = os.getenv("LOCAL_PRODUCER_SLEEP_TIME", 0.1)  # when there are no new log lines
    LOCAL_PRODUCER_DELIMITER = os.getenv("LOCAL_PRODUCER_DELIMITER", ",")

    # High traffic alert constants
    HIGH_TRAFFIC_TIME_INTERVAL = os.getenv("HIGH_TRAFFIC_TIME_INTERVAL", 120)  # range in seconds
    HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND = os.getenv("HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND", 10)
    HIGH_TRAFFIC_MAX_REQUESTS_PER_INTERVAL = HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND * HIGH_TRAFFIC_TIME_INTERVAL

    # High traffic alert notification constants
    HIGH_TRAFFIC_ALERT_NOTIFICATION_MESSAGE = os.getenv("HIGH_TRAFFIC_ALERT_NOTIFICATION_MESSAGE",
                                                        "High traffic generated an alert - hits = {value},"
                                                        " triggered at {time}")
    HIGH_TRAFFIC_RECOVERY_NOTIFICATION_MESSAGE = os.getenv("HIGH_TRAFFIC_RECOVERY_NOTIFICATION_MESSAGE",
                                                           "traffic recovered at {time}")
    HIGH_TRAFFIC_ALERT_NOTIFICATION_LEVEL = os.getenv("HIGH_TRAFFIC_ALERT_NOTIFICATION_LEVEL", "CRITICAL")
    HIGH_TRAFFIC_ALERT_NOTIFICATION_TYPE = os.getenv("HIGH_TRAFFIC_ALERT_NOTIFICATION_TYPE", "ALERT")
    HIGH_TRAFFIC_RECOVERY_NOTIFICATION_LEVEL = os.getenv("HIGH_TRAFFIC_RECOVERY_NOTIFICATION_LEVEL", "CRITICAL")
    HIGH_TRAFFIC_RECOVERY_NOTIFICATION_TYPE = os.getenv("HIGH_TRAFFIC_RECOVERY_NOTIFICATION_TYPE", "RECOVERY")

    # stats constants
    TRAFFIC_STATS_TIME_INTERVAL = os.getenv("TRAFFIC_STATS_TIME_INTERVAL", 10)  # range in seconds
    TRAFFIC_STATS_NOTIFICATION_LEVEL = os.getenv("HIGH_TRAFFIC_ALERT_NOTIFICATION_LEVEL", "INFO")
    TRAFFIC_STATS_NOTIFICATION_TYPE = os.getenv("HIGH_TRAFFIC_ALERT_NOTIFICATION_TYPE", "STATS")
    TRAFFIC_STATS_NOTIFICATION_MESSAGE = os.getenv("TRAFFIC_STATS_NOTIFICATION_MESSAGE",
                                                   f"Statistic for last {TRAFFIC_STATS_TIME_INTERVAL} "
                                                   "seconds triggered at {time}:\n"
                                                   "{stats}")

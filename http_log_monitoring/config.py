import os


class Config:
    # Common constants
    DATETIME_FORMAT = os.getenv("DATETIME_FORMAT", '%Y-%m-%d %H:%M:%S')

    # High traffic alert constants
    HIGH_TRAFFIC_TIME_INTERVAL = os.getenv("HIGH_TRAFFIC_TIME_INTERVAL", 120)  # range in seconds
    HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND = os.getenv("HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND", 10)
    HIGH_TRAFFIC_ALERT_MESSAGE = os.getenv("HIGH_TRAFFIC_ALERT_MESSAGE",
                                           "High traffic generated an alert - hits = {value}, triggered at {time}")
    HIGH_TRAFFIC_RECOVERY_MESSAGE = os.getenv("HIGH_TRAFFIC_RECOVERY_MESSAGE",
                                              "traffic recovered at {time}")
    HIGH_TRAFFIC_MAX_REQUESTS_PER_INTERVAL = HIGH_TRAFFIC_MAX_REQUESTS_PER_SECOND * HIGH_TRAFFIC_TIME_INTERVAL

    # stats constants
    TRAFFIC_STATS_TIME_INTERVAL = os.getenv("TRAFFIC_STATS_TIME_INTERVAL", 10)  # range in seconds
    

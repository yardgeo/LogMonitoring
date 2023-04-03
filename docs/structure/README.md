# Project structure

Project structure is represented bellow.

```bash
.
├── README.md
├── data
│   ├── sample_csv.txt
│   ├── sample_csv_original.txt
│   └── test_csv.txt
├── docs
│   ├── design
│   │   ├── README.md
│   │   └── design.png
│   ├── following_steps
│   │   └── README.md
│   ├── installation
│   │   └── README.md
│   ├── problem.pdf
│   └── structure
│       └── README.md
├── http_log_monitoring
│   ├── Dockerfile
│   ├── __init__.py
│   ├── config.py
│   ├── consumers
│   │   ├── __init__.py
│   │   ├── common_notification_consumer.py
│   │   └── console_notification_consumer.py
│   ├── dispatcher.py
│   ├── dto
│   │   ├── __init__.py
│   │   ├── log_line.py
│   │   ├── notfication.py
│   │   └── stats
│   │       ├── __init__.py
│   │       ├── bytes_stats.py
│   │       ├── common_stats.py
│   │       ├── request_stats.py
│   │       └── status_stats.py
│   ├── exceptions
│   │   ├── __init__.py
│   │   └── log_line_parsing_exception.py
│   ├── hadnlers
│   │   ├── __init__.py
│   │   ├── alerts
│   │   │   ├── __init__.py
│   │   │   └── high_traffic_alert_handler.py
│   │   ├── log_line_handler.py
│   │   └── stats
│   │       ├── __init__.py
│   │       ├── traffic_stats_handler.py
│   │       └── traffic_stats_handler_state.py
│   ├── main.py
│   ├── producers
│   │   ├── __init__.py
│   │   ├── http_log_producer.py
│   │   └── local_csv_file_http_log_producer.py
│   ├── requirements.txt
│   ├── setup.py
│   ├── test.Dockerfile
│   ├── tests
│   │   ├── __init__.py
│   │   ├── generators
│   │   │   ├── __init__.py
│   │   │   └── real_time_data_generator.py
│   │   ├── test_console_notification_consumer.py
│   │   ├── test_dispatcher.py
│   │   ├── test_high_traffic_alert_handler.py
│   │   ├── test_local_csv_file_http_log_producer.py
│   │   ├── test_log_line.py
│   │   ├── test_traffic_stats_handler.py
│   │   ├── test_traffic_stats_handler_state.py
│   │   └── test_utils
│   │       ├── __init__.py
│   │       └── dataclass_utils.py
│   └── utils
│       ├── __init__.py
│       ├── custom_logger_formatter.py
│       └── dataclass_utils.py
├── run_app_docker.sh
└── run_tests_docker.sh

33 directories, 98 files

```

* data directory contains data files which are used by the program
* docs directory contains documents and instruction of the project
* http_log_monitoring/config.py contains all constants for the project
* http_log_monitoring/tests directory contains unit tests for the project
* http_log_monitoring/utils directory contains utils functions for the project
* http_log_monitoring/dto directory contains Data Transfer Objects for the
  project
    * LogLineDto contains information about one line of the http log
    * NotificationDro contains information about notification
    * stats directory contains information about different statistical sections
* http_log_monitoring/consumers directory contains Notification consumer
  classes
* http_log_monitoring/producers directory contains Log Line producer classes
* http_log_monitoring/handlers directory contains Log Line handler classes
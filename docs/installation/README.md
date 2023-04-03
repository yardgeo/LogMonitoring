# Installation and running guide

## Pre-Requirements

* Unix-like operating system
* Python (version 3.11+) installed **or/and**
* Docker (version 19.03.4+) installed

## Install the program

1. Download zip-archive of the project
2. Unzip the archive
3. Change directory to project home directory

Example:

```bash
unzip LogMonitoring
cd LogMonitoring
```

## Run the program

To run the program with Docker **[preferable]**:

```bash
chmod +x run_app_docker.sh
bash run_app_docker.sh [-f file] [-i]
```

Script options:

* -f specify file path to log file. **Important**: the file must be located in
  the data directory of the project. By default, set to sample_csv.txt.
* if -i flag is set, the application will run in online mode. In that mode the
  program won't stop after reading all lines of the log file and will wait for
  online file updates. The program can be safely stopped by user using Cntr+C
  command. By default, set to False.

To run the program without Docker:

```bash
python http_log_monitoring/main.py
```

It is possible to specify log file as a parameter:

```bash
python http_log_monitoring/main.py data/sample_csv.txt
```

## Run unit tests

To run unit tests with Docker **[preferable]**:

```bash
chmod +x run_tests_docker.sh
./run_tests_docker.sh
```

To run unit tests without Docker:

```bash
cd http_log_monitoring
python -m unittest discover -v
```

# Installation and running guide

## Pre-Requirements
* Unix-like operating system
* Python (version 3.8+) installed **or/and**
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
./run_app_docker.sh
```
To run the program without Docker:
```bash
python http_log_monitoring/main.py
```
It is possible to specify log file as a parameter:
```bash
python http_log_monitoring/main.py data/sample_csv.txt
```

## Test the program
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

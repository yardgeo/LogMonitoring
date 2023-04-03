#!/bin/bash

OFFLINE_MODE=true

# check if argument was passed
while getopts 'if:' OPTION; do
  case "$OPTION" in
    f)
      FILE_NAME=$OPTARG
      ;;
    i)
      echo "The application will run in online mode"
      OFFLINE_MODE=false
      ;;
    ?)
      echo "script usage: $(basename $0) [-f file] [-i]" >&2
      exit 1
      ;;
  esac
done
shift "$(($OPTIND -1))"

if [ -z "$FILE_NAME" ]
  then
    echo "Csv log file wasn't provided, try to use data/sample_csv.txt"
    FILE_NAME=data/sample_csv.txt
fi

sleep 1

# check if file exist in local data directory
BASE_NAME=$(basename ${FILE_NAME})
if [ -e $(pwd)/data/"$BASE_NAME" ]; then
   echo "Building local docker image..."
    docker build -t log_monitoring http_log_monitoring
    echo "Image is built"
    echo "Starting docker container..."
    docker run --rm -v $(pwd)/data:/data --env LOCAL_PRODUCER_FILEPATH=/data/"$BASE_NAME" --env LOCAL_PRODUCER_OFFLINE_MODE="$OFFLINE_MODE" -it log_monitoring
    echo "Docker container is stopped"
    echo "Docker container is removed"
else
  echo "File "$BASE_NAME" does not exist in "$(pwd)"/data directory"
fi

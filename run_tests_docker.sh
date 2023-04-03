#!/bin/bash
docker build -t log_monitoring_test -f http_log_monitoring/test.Dockerfile http_log_monitoring
docker run --rm -v $(pwd)/data:/data --env LOCAL_PRODUCER_FILEPATH=/data/sample_csv.txt -it log_monitoring_test
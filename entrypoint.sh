#!/bin/bash

set -ex

sed -i 's/ERR_LOG/'"${LOG_LEVEL:=ERROR}"'/g' /app/logger.conf
sed -i 's/ACC_LOG/'"${ACCESS_LOG_LEVEL:=INFO}"'/g' /app/logger.conf

gunicorn \
    --worker-tmp-dir=/dev/shm \
    --worker-class=${GUNICORN_WORKER_CLASS:=gthread}  \
    --workers=${GUNICORN_WORKERS:=2} \
    --threads=${GUNICORN_THREADS:=4} \
    --bind=0.0.0.0:5000 \
    --log-config=logger.conf \
    app:app
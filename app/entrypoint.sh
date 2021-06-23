#!/bin/bash

while ! nc -z "$POSTGRES_HOST" "5432"; do
  sleep 0.1
done

exec python3.8 run.py
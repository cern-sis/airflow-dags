#!/bin/bash
# Initialize the database
airflow db init

# Run the original entrypoint command
exec "$@"

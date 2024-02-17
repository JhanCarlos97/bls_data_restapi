#!/bin/bash

# Generate JWT secret key
echo "Generating JWT secret key..."
python utils/generate_jwt_secret.py

# Start PostgreSQL and PostgREST containers
echo "Starting containers"
docker-compose up -d

# Wait for containers to start
echo "Waiting for containers to start..."
sleep 10

# Execute data ingestion script
# echo "Running ingest process by streaming"
# python utils/data_ingestion_stream.py

# Or as a batch if you want
echo "Running ingest process by batch"
python utils/data_ingestion_batch.py
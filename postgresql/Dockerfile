# Use the official PostgreSQL base image
FROM postgres:latest

# Set the working directory
WORKDIR /usr/src/app

# Copy the .env file to the working directory
COPY .env .env

# Load environment variables from the .env file
ENV $(cat .env | xargs)

# Copy the initialization SQL script to the container
COPY postgresql/init.sql /docker-entrypoint-initdb.d/init.sql

# Expose the default PostgreSQL port
EXPOSE ${POSTGRES_PORT}
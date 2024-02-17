import os
import psycopg2
import re
from io import StringIO
from dotenv import load_dotenv
from constants import file_references
import logging

# To remove the HTTP calls (if you need to check the API call made, remove this line)
# logging.getLogger("httpx").setLevel(logging.WARNING)

# Configure logging
logging.basicConfig(level=logging.INFO)

class PostgreSQLConnection:
    def __init__(self, db_uri):
        self.db_uri = db_uri
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(self.db_uri)
            self.cursor = self.conn.cursor()
        except psycopg2.Error as e:
            logging.INFO("Error connecting to PostgreSQL:", e)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

def parse_env_variables():
    load_dotenv("../.env")
    return {
        "postgres_user": os.getenv("POSTGRES_USER"),
        "postgres_password": os.getenv("POSTGRES_PASSWORD"),
        "postgres_db": os.getenv("POSTGRES_DB"),
        "postgres_host": os.getenv("POSTGRES_HOST"),
        "postgres_port": os.getenv("POSTGRES_PORT"),
        "postgres_schema": os.getenv("POSTGRES_SCHEMA"),
        "postgrest_jwt_secret": os.getenv("POSTGREST_JWT_SECRET")
    }

def construct_db_uri(env_variables):
    return f"postgres://{env_variables['postgres_user']}:{env_variables['postgres_password']}@" \
           f"{env_variables['postgres_host']}:{env_variables['postgres_port']}/{env_variables['postgres_db']}"

def load_data_into_postgres(file_path, schema, table_name, cursor, conn):
    logging.info(f"Loading data into {schema}.{table_name}")
    with open(file_path, "r") as f:
        # Read the first line to get column names
        header = next(f).strip().split('\t')
        num_columns = len(header)

        # Iterate over the remaining lines
        for line in f:
            # Split the line into columns and trim whitespaces
            columns = [col.strip() for col in line.strip().split('\t')]

            # Clean up values with extra spaces
            columns = [re.sub(r'\s+', ' ', col) for col in columns]

            # Check if the number of columns matches the number of columns in the header
            if len(columns) < num_columns:
                columns.extend([''] * (num_columns - len(columns)))

            # Construct the COPY command
            copy_command = f"COPY {schema}.{table_name} ({', '.join(header)}) FROM STDIN WITH CSV DELIMITER E'\\t' NULL AS ''"

            # Create a file-like object to mimic the behavior of a file
            data = StringIO('\t'.join(str(col) if col is not None else '' for col in columns) + '\n')

            # Execute the COPY command with data
            cursor.copy_expert(copy_command, data)

            # Commit the changes after each row is copied
            conn.commit()

def main():
    # Parse environment variables
    env_variables = parse_env_variables()

    # Construct db-uri
    db_uri = construct_db_uri(env_variables)
    logging.info(f"Connecting to PostgreSQL database: {db_uri}")

    # Connect to PostgreSQL
    pg_conn = PostgreSQLConnection(db_uri)
    pg_conn.connect()

    # Download and ingest data
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    for table_name, file_name in file_references:
        file_path = os.path.join(data_dir, f"{file_name}.txt")
        schema = env_variables.get("postgres_schema", "public")
        load_data_into_postgres(file_path, schema, table_name, pg_conn.cursor, pg_conn.conn)

    logging.info("Data ingestion completed.")
    
    # Close connection
    pg_conn.close()

    logging.info("Connection to PostgreSQL database closed.")

if __name__ == "__main__":
    main()
import os
import http.client
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
POSTGREST_HOST = os.getenv("POSTGREST_HOST")
POSTGREST_PORT = os.getenv("POSTGREST_PORT")

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_data_from_postgrest(endpoint):
    # Establish connection to PostgREST server
    logging.info(f"Connecting to PostgREST server at {POSTGREST_HOST}:{POSTGREST_PORT}")
    connection = http.client.HTTPConnection(POSTGREST_HOST, POSTGREST_PORT)

    # Send GET request to specified endpoint
    logging.info(f"Sending GET request to endpoint: {endpoint}")
    connection.request("GET", endpoint)

    # Get response from server
    response = connection.getresponse()

    # Read and decode response data
    data = response.read().decode()

    # Close connection
    connection.close()

    return data

def main():

    # List of endpoints availables
    # Feel free to play, test and check their output :)

    endpoints = ["/women_in_goverment_v1",
                 "/women_in_goverment_v2",
                 "/ratio_production_supervisory"
                ]
    for endpoint in endpoints:
        logging.info(f"Fetching data from endpoint: {endpoint}")
        data = get_data_from_postgrest(endpoint)
        logging.info(f"Received data: {data}")

if __name__ == "__main__":
    main()
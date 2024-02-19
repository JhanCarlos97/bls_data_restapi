# BLS Data REST API Project

This project aims to create a RESTful API for accessing and managing data from the Bureau of Labor Statistics (BLS).

## Overview

The BLS Data REST API project facilitates easy access to BLS data through a RESTful interface. It includes functionality for ingesting data from various sources, processing and transforming the data, and exposing it through a user-friendly API.

## Features

- **Data Ingestion**: Automates the process of ingesting data from external sources into a PostgreSQL database.
- **Data Transformation**: Cleans and transforms raw data to prepare it for API consumption.
- **API Integration**: A RESTful API for accessing BLS data, based on PostgREST API, that provides endpoints for querying data about "Women in government" or the ratio "production employees / supervisory employees" during different time periods.
- **Containerized Deployment**: Utilizes Docker containers for easy deployment and scaling.

### Limitation

- Due to the nature of the source, the BLS prohibits automated processes that make requests to their data. This limitation prompted us to move from an automated approach to using downloaded local files instead, stored in the `data/` folder.
- Additionally, due to the size of these files and the limitations on the size of files a repository can have (over 100 MB), we encourage users to download the required file `ce.data.0.AllCESSeries` from <https://download.bls.gov/pub/time.series/ce/> and replace it locally, just in the case you are grabbing the project from the remote repo.

## Requirements

- Python 3.x and pipenv (for virtual environment)
- Docker and Docker Compose

## Installation

1. Start the local environment using pipenv command from the command line interface (CLI):

   ```bash
   pipenv shell

This command will create a virtual environment and install all the required dependencies from the Pipfile.lock file.

2. Update your .env file, if needed


## Usage

The usage of this project is straightforward and is handled by three main scripts:

- `run.sh`
- `test_api.sh`
- `clean.sh`

These scripts automate the most important steps of the project: setup, testing, and removal of resources. Let's proceed with the details:

1. Start the project using the `run.sh` script:

   ```console
   ./run.sh
   ```

This script creates the necessary resources for your local PostgreSQL database using Docker, ensuring compatibility and version consistency. It sets up tables, schemas, views, roles, and users required for the PostgREST API usage.

Additionally, the script handles the implementation of the PostgREST API, eliminating the need for manual installation on your machine. After setting up the resources, it executes either `utils/data_ingestion_batch.py` or `utils/data_ingestion_stream.py` depending of its content.

As of now, `utils/data_ingestion_batch.py` is executed, which ingests data in "mini" batches of *3000* rows to avoid potential memory issues. If you prefer the streaming approach, i.e., ingesting row by row, you can modify `run.sh` accordingly before running it (instructions provided in the script).

2. Once the data and the PostgREST API are available, you can test the API by running the `test_api.sh` script:

   ```console
   ./test_api.sh
    ```

This script triggers the `utils/data_api_connect.py` which connects to port `3000` on localhost to make a GET request to the API. You will see the following output on the console:

        ...
        INFO:root:Sending GET request to endpoint: /women_in_goverment_v1
        INFO:root:Received data: [{"date":"January 1964","valueInThousands":3640},
        {"date":"February 1964","valueInThousands":3655},
        {"date":"March 1964","valueInThousands":3674},
        {"date":"April 1964","valueInThousands":3698},
        {"date":"May 1964","valueInThousands":3720},
        ...
        {"date":"January 2024","valueInThousands":13493}]

** Alternatively, individual API calls can be made directly from the command line interface using:

        curl localhost:3000/women_in_goverment_v1

3. Finally, to clean and remove all the resources used by the project, execute:

   ```console
   ./clean.sh
    ```

This script removes volumes, containers and images created for the database and API implementation.

### Endpoints

We have 3 endpoints implemented:

1. `women_in_goverment_v1`
2. `women_in_goverment_v2`
3. `ratio_production_supervisory`

1. `women_in_goverment_v1`

- This endpoint utilizes data from the `ce.data.0.AllCESSeries.txt` file, which was ingested into the `public.all_ces` table.
- A view named `women_in_goverment_v1` was created under the `api_call` schema. This view filters data based on specific `series_id` references related to women.

2. `women_in_goverment_v2`

- Data for this endpoint is sourced from the `ce.data.90a.Government.Employment.txt` file, ingested into the `public.ce_government` table.
- Similar to the first endpoint, a view named `women_in_goverment_v2` under the `api_call` schema was created. It filters data based on specific `series_id` references related to women. This dataset is a subset of the data in `public.all_ces` and may be preferable for larger volumes of data.

3. `ratio_production_supervisory`

- This endpoint utilizes data from the `ce.data.0.AllCESSeries.txt` and `ce.supersector.txt` files.
- Data from the `ce.supersector.txt` file was ingested into the public.ce_supersector table.
- A view named `ratio_production_supervisory` under the `api_call` schema was created. This view filters data from `public.all_ces` to calculate the ratio between `all_employees` and `production_and_non_supervisory_employees`. Additionally, it matches `supersector_code` from the `series_id` with data in `public.ce_supersector` to provide the supersector name.

## Adding New Endpoints

To introduce new endpoints:
1. Connect to your local database and create any necessary views.
2. If starting from scratch, add the required views to `postgresql/init.sql` before executing the `run.sh` script.
3. Ensure that the `PostgREST API` role and user have appropriate permissions on the newly created views.

Feel free to customize these instructions based on your project's specific structure and requirements.

## Project Status

This project was developed to address specific requirements within a given timeframe. While the main focus was on delivering a functional solution, there are areas for potential improvement in code quality and structure.

### Areas for Improvement

- Code Structure: The current organization meets the immediate requirements but may benefit from refactoring to enhance readability and maintainability.
- Documentation: The project strives to provide clear and concise documentation; however, there's room for improvement in the depth and coverage of code, comments and explanations.

### Consideration for Timely Delivery

Given the nature of the project and the specified timeframe, the primary goal was to deliver a working solution. Appreciation is extended for understanding this approach, and any feedback or suggestions for improvement are welcomed.

Contributions and feedback are appreciated to help enhance the project further. Insights and recommendations are valuable, and the project is open to making refinements based on those suggestions.
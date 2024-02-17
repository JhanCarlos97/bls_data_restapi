# BLS Data REST API Project

This project aims to create a RESTful API for accessing and managing data from the Bureau of Labor Statistics (BLS).

## Overview

The BLS Data REST API project facilitates easy access to BLS data through a RESTful interface. It includes functionality for ingesting data from various sources, processing and transforming the data, and exposing it through a user-friendly API.

## Features

- **Data Ingestion**: Automates the process of ingesting data from external sources into a PostgreSQL database.
- **Data Transformation**: Cleans and transforms raw data to prepare it for API consumption.
- **API Integration**: A RESTful API for accessing BLS data, based on PostgREST API, that provides endpoints for querying data about "Women in goverment" or ratio "production employees / supervisory employees" 
during time
- **Containerized Deployment**: Utilizes Docker containers for easy deployment and scaling.

### Limitation

- Due to the nature of the source, the BLS prohibites automated processes that makes requests to their data. It pushed us to move from an automated approach to use downloaded local files instead, at the `data/` folder.

## Requirements

- Python 3.x and pipenv (for virtual environment)
- Docker and Docker Compose

## Installation

1. Start the local environment using pipenv command from CLI:

   ```bash
   pipenv shell

This command will create a virtual environment and grab all the dependencies from the Pipfile.lock file.

2. Update your .env file, if needed


## Usage

The way to implement this is straight forward. There're three files:

- `run.sh`
- `test_api.sh`
- `clean.sh`

Each of them handles the most important steps on the project: setup, test and remove any resource. Let's move on!

1. Start the project using the `run.sh` script:

   ```console
   ./run.sh
   ```

This files creates the resources for your own local Postgresql database with Docker, without worring about version issues or compatibility, by creating all the tables, schemas, views, roles and users that will be needed for the PostgREST API usage.

And, of course, it handles the PostgREST API implementation, without worring about any instalation on your machine.

After all those resources are created, it runs the `utils/data_ingestion_batch.py` or `utils/data_ingestion_stream.py` depending of the content of it.

As of now, the first one is the one to be executed, it ingest the data in "mini" batches of `3000` rows so we won't face any potential memory issue, but, if you want to follow the stream approach i.e. ingesting row by row, go and modify the `run.sh` before running it (instructions on it explaining this!).

2. After the previous step, we will have data available and the PostgREST API too, so, we can start making call to it by running `test_api.sh` script:

   ```console
   ./test_api.sh
    ```

The script will trigger the `utils/data_api_connect.py` that connects to the port `3000` at localhost, to make the GET request to the API and, you will see the following output on the console:

        ...
        INFO:root:Sending GET request to endpoint: /women_in_goverment_v1
        INFO:root:Received data: [{"date":"January 1964","valueInThousands":3640},
        {"date":"February 1964","valueInThousands":3655},
        {"date":"March 1964","valueInThousands":3674},
        {"date":"April 1964","valueInThousands":3698},
        {"date":"May 1964","valueInThousands":3720},
        ...
        {"date":"January 2024","valueInThousands":13493}]

** Alternative usage for individual API calls could be, directly into your CLI like this:

        curl localhost:3000/women_in_goverment_v1

3. And finally, to clean and remove all the resources used for the project, we will run:

   ```console
   ./clean.sh
    ```

This will remove volumes, containers and images created for the db + API implementation.

### Endpoints

We have 3 endpoints implemented:

1. `women_in_goverment_v1`
2. `women_in_goverment_v2`
3. `ratio_production_supervisory`

The first one, `women_in_goverment_v1`, uses the data that came from the `ce.data.0.AllCESSeries.txt` file. It was ingested in the `public.all_ces` and a view at the `api_call` schema, called `women_in_goverment_v1` was created. This view filters some `series_id` data that references the "women" on it.

The second one, `women_in_goverment_v2`, uses the data that came from the `ce.data.90a.Government.Employment.txt` file. It was ingested in the `public.ce_government` and a view at the `api_call` schema, called `women_in_goverment_v2` was created. This view filters some `series_id` data that references the "women" on it. This data is a subset of the data in `public.all_ces` that, for higher volumes, could be a suitable option to grab the data instead.

The third one, `ratio_production_supervisory`, uses the data that came from the `ce.data.0.AllCESSeries.txt` file and `ce.supersector.txt` file. The supersector was ingested in the `public.ce_supersector` and a view at the `api_call` schema, called `ratio_production_supervisory` was created. This view filters the data from the `public.all_ces` by grabbing the `all_employees` records and the `production_and_non_supervisory_employees` records to calculate the ratio. Plus, we grab the `supersector_code` from the `series_id` to match them with the `public.ce_supersector` to output the supersector name.

## Adding New Endpoints

To add new endpoints, you can connect to your local database and create any view needed or, if you want to recreate them from scratch, just add it to the `postgresql/init.sql` before running the `run.sh` file and verify the correct permissions for the `PostgREST API` role and user on those new views.

Feel free to customize the instructions based on your specific project structure and requirements.

## Project Status

This project was developed to address specific requirements within a given timeframe. While the main focus was on delivering a functional solution, there are areas for potential improvement in code quality and structure.

### Areas for Improvement

- Code Structure: The current organization meets the immediate requirements but may benefit from refactoring to enhance readability and maintainability.
- Documentation: The project strives to provide clear and concise documentation; however, there's room for improvement in the depth and coverage of code, comments and explanations.

### Consideration for Timely Delivery

Given the nature of the project and the specified timeframe, the primary goal was to deliver a working solution. Appreciation is extended for understanding this approach, and any feedback or suggestions for improvement are welcomed.

Contributions and feedback are appreciated to help enhance the project further. Insights and recommendations are valuable, and the project is open to making refinements based on those suggestions.
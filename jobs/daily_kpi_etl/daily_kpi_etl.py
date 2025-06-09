#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
home = PosixPath('/Users/doron/workspace')

"""

from pathlib import Path
import os
import requests
from google.cloud import bigquery
client = bigquery.Client()

project_id = "bi-course-461012"

# adapt the env to mac or windows
if os.name == 'nt':
    home = Path("C:/workspace/")
else:
    home = Path(os.path.expanduser("~/workspace/"))


def ensureDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def readFile(fileName):
    with open(fileName, "r") as file:
        data = file.read()
        file.close()
    return data

def writeFile(fileName, Data):
    with open(fileName, "w", newline='', encoding='utf-8') as file:
    # with open(fileName, "w", encoding='utf-8') as file:
        file.write(Data)
    file.close()


print("Extract")

# Define the API endpoint and any necessary headers (if required)
api_url = "https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.csv"
# headers = {
#     "Authorization": "Bearer YOUR_API_KEY",  # Use if an API key or token is required
#     "Content-Type": "application/json"
# }

# Function to extract data from the API
def extract_data_from_api(url, headers=None):
    try:
        # Send a GET request to the API
        response = requests.get(url, headers=headers)

        # Check if the response is successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            # data = response.json()
            data = response.text
            return data
        else:
            # Handle non-successful response
            print(f"Failed to retrieve data: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        # Handle any request-related errors
        print(f"An error occurred: {e}")
        return None

# Call the function to extract data
data = extract_data_from_api(api_url)

# Print the extracted data (for testing purposes)
# if data:
#     # print(json.dumps(data, indent=4))
#     print(data)

# write data to file
date_file = home / "temp/data/bi/jobs/my_etl/us-states.csv"
ensureDirectory( home / "temp/data/bi/jobs/my_etl/")
writeFile(date_file, data)

##video1
"""print("Extract the file")
# file_name = "/Users/doron/workspace/bi/jobs/daily_kpi_etl/daily_kpi_etl.py"         #folder name non-dynamic
python_file_name = "daily_kpi_etl"
file_name_2 = home / "bi/jobs/daily_kpi_etl/daily_kpi_etl.py"                           #folder name dynamic
ensureDirectory(home / f"temp/data/bi/jobs/{python_file_name}")
data_folder = home / f"temp/data/bi/jobs/{python_file_name}"
data_file = data_folder / "us-states.csv"
"""




print("Transform")
print("Load")

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"
table_id = f"{project_id}.my_etl.us_states_csv"

job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("name", "STRING"),
        bigquery.SchemaField("post_abbr", "STRING"),
    ],
    # write_disposition="WRITE_TRUNCATE",
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    skip_leading_rows=1,
    # The source format defaults to CSV, so the line below is optional.
    source_format=bigquery.SourceFormat.CSV,
)


with open(date_file, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

job.result()  # Waits for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(
    f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}"
    )
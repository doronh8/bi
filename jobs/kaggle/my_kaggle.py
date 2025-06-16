#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""
repo_name = bi
repo_tail = jobs/kaggle/
home = /Users/doron/workspace


python3 bi/jobs/kaggle/my_kaggle.py bi-course-461012 --etl-name etl --etl-action daily

"""


from pathlib import Path
import os
import requests
import json
import re
import sys
from google.cloud import bigquery
import argparse
from datetime import datetime, timedelta, date
import uuid
import platform
import pandas as pd
from matplotlib import pyplot as plt
from kaggle.api.kaggle_api_extended import KaggleApi


# adapt the env to mac or windows
if os.name == 'nt':
    home = Path("C:/workspace/")
else:
    home = Path(os.path.expanduser("~/workspace/"))


# get repository name
repo_name = re.search(r"(.*)[/\\]workspace[/\\]([^/\\]+)", __file__).group(2)
repo_tail = re.search(r".*[/\\]"+repo_name+r"[/\\](.+)[/\\]", __file__).group(1)
sys.path.insert(0, str(home / f"{repo_name}/utilities/"))

from my_etl_files import readJsonFile, ensureDirectory, writeFile, readFile

def process_command_line(argv):
    if argv is None:
        argv = sys.argv[1:]
    # initialize the parser object:

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id",
                        help="""Operation to perform. The arguments for each option are:
                        Full_Load:   --date""",
                        default="bi-course-461012")
    parser.add_argument("--etl-action", choices=["init", "daily", "delete"], help="""The action the etl job""")
    parser.add_argument("--etl-name", help="""The name of the etl job""")
    parser.add_argument("--dry-run", help="""if True don't execute the queries""", action="store_true")
    parser.add_argument("--days-back", help="""The number of days we want to go back""",
                        default=1)

    return parser, argparse.Namespace()


parser, flags = process_command_line(sys.argv[1:])
x = sys.argv[1:]
parser.parse_args(x, namespace=flags)

# define the project_id
project_id = flags.project_id
etl_name = flags.etl_name
etl_action = flags.etl_action
days_back = int(flags.days_back)

step_id = 0
env_type = 'daily'
log_table = f"{project_id}.logs.daily_logs"


# Construct a BigQuery client object.
client = bigquery.Client(project=project_id)

# Get dates
date_today = date.today()
y_m_d = (date_today + timedelta(days=-days_back)).strftime("%Y-%m-%d")
ymd = y_m_d.replace("-", "")


# init log dict
log_dict = {'ts': datetime.now(),
            'dt': datetime.now().strftime("%Y-%m-%d"),
            'uid': str(uuid.uuid4())[:8],
            'username': platform.node(),
            'job_name': etl_name,
            'job_type': etl_action,
            'file_name': os.path.basename(__file__),
            'step_name': 'start',
            'step_id': step_id,
            'log_type': env_type,
            'message': str(x)
            }


# functions
def set_log(log_dict, step, log_table=log_table):
    log_dict['step_name'] = step
    log_dict['step_id'] += 1
    log_dict['ts'] = datetime.now()
    log_dict['dt'] = datetime.now().strftime("%Y-%m-%d")
    job = client.load_table_from_dataframe(pd.DataFrame(log_dict, index=[0]), log_table)
    job.result() # Wait for the job to complete.


if not flags.dry_run:
    set_log(log_dict, "start")

print('a')
# get etl configuration
etl_configuration = readJsonFile(home / repo_name / repo_tail / f"config/{etl_name}_config.json")
# etl_conf = readJsonFile(home / "bi/jobs/kaggle/screen_time_impact_on_mental_health/config/etl_config.json")["screen_time_impact_on_mental_health"]
print('b')

for etl_name, etl_conf in etl_configuration.items():
        if not etl_conf["isEnable"]:
            continue
        print(f"{etl_name}\n{len(etl_name)*'='}\n")

        print("Extract")

        if not flags.dry_run:
            set_log(log_dict, f"Extract {etl_name}")


        # Kaggle dataset info
        # "abhishekdave9/digital-habits-vs-mental-health-dataset"

        # Define target path
        target_path = os.path.expanduser(home / f"temp/data/{etl_conf["data_folder"]}")

        # Make sure the target directory exists
        os.makedirs(target_path, exist_ok=True)

        # Set up the API
        api = KaggleApi()
        api.authenticate()
        print('c')

        # Dataset identifier from Kaggle
        dataset = f"{etl_conf["producer"]}/{etl_conf["dataset_name"]}"
        # dataset = "abhishekdave9/digital-habits-vs-mental-health-dataset"

        # Download and unzip the dataset into the target directory
        api.dataset_download_files(dataset, path=target_path, unzip=True)

        print('d')
        # Function to extract data from the API
        def extract_data_from_api(url, headers=None):
            try:
                # Send a GET request to the API
                response = requests.get(url, headers=headers)
                # Check if the response is successful (status code 200)
                if response.status_code == 200:
                    # Parse the JSON response
                    data = response.text
                    return data
                else:
                    # Handle non-successful response
                    error_msg = print(f"Failed to retrieve data: {response.status_code} - {response.text}")
                    if not flags.dry_run:
                        log_dict["message"] = error_msg
                        set_log(log_dict, f"Error in Extract {etl_name}")
                        log_dict["message"] = str(x)
                    return None

            except requests.exceptions.RequestException as e:
                # Handle any request-related errors
                error_msg = f"An error occurred: {e}"
                print(error_msg)
                if not flags.dry_run:
                    log_dict["message"] = error_msg
                    set_log(log_dict, f"Error in API Extract {etl_name}")
                    log_dict["message"] = str(x)
                return None

        print('e')

        # List the downloaded files to verify
        print("Files in target directory:", os.listdir(target_path))

        print("Transform")

        data_file = f"{target_path}/{etl_conf["file_name"]}"


        # Clean column headers: replace spaces with underscores
        df = pd.read_csv(data_file)
        original_columns = df.columns.tolist()
        df.columns = [col.strip().replace(" ", "_") for col in df.columns]
        df.to_csv(data_file, index=False)

        print("Column headers cleaned:")
        for old, new in zip(original_columns, df.columns):
            if old != new:
                print(f"  '{old}' → '{new}'")
        if not flags.dry_run:
            set_log(log_dict, f"Transform {etl_name}")
        print("Load")
        if not flags.dry_run:
            set_log(log_dict, f"Load {etl_name}")

        # TODO(developer): Set table_id to the ID of the table to create.
        # table_id = "your-project.your_dataset.your_table_name"
        table_id = etl_conf["table_id"]

        job_config = bigquery.LoadJobConfig(
            autodetect=True,
            # write_disposition="WRITE_TRUNCATE",
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
            skip_leading_rows=1,
            # The source format defaults to CSV, so the line below is optional.
            source_format=bigquery.SourceFormat.CSV,
        )

        with open(data_file, "rb") as source_file:
            job = client.load_table_from_file(source_file, table_id, job_config=job_config)

        job.result()  # Waits for the job to complete.

        table = client.get_table(table_id)  # Make an API request.
        msg = f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}"
        print(msg)
        if not flags.dry_run:
            log_dict["message"] = msg
            set_log(log_dict, f"Load finished {etl_name}")
            log_dict["message"] = str(x)

if not flags.dry_run:
    set_log(log_dict, "end")



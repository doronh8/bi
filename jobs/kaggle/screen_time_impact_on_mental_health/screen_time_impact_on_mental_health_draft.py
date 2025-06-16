#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""""
repo_name = bi
repo_tail = jobs/kaggle/screen_time_impact_on_mental_health
home = /Users/doron/workspace

"""


import re
import sys
from pathlib import Path
import os
import requests
import json
from kaggle.api.kaggle_api_extended import KaggleApi
from google.cloud import bigquery
import pandas as pd
from matplotlib import pyplot as plt


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


# get etl configuration
etl_conf = readJsonFile(home / repo_name / repo_tail / "config/etl_config.json")["screen_time_impact_on_mental_health"]
# etl_conf = readJsonFile(home / "bi/jobs/kaggle/screen_time_impact_on_mental_health/config/etl_config.json")["screen_time_impact_on_mental_health"]

print("Extract")



print("Extract the file")

# Kaggle dataset info
# "abhishekdave9/digital-habits-vs-mental-health-dataset"

# Define target path
target_path = os.path.expanduser(home / f"temp/data/{etl_conf["data_folder"]}")

# Make sure the target directory exists
os.makedirs(target_path, exist_ok=True)

# Set up the API
api = KaggleApi()
api.authenticate()


# Dataset identifier from Kaggle
dataset = f"{etl_conf["producer"]}/{etl_conf["dataset_name"]}"
# dataset = "abhishekdave9/digital-habits-vs-mental-health-dataset"

# Download and unzip the dataset into the target directory
api.dataset_download_files(dataset, path=target_path, unzip=True)

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


print("Load")

# Construct a BigQuery client object.
client = bigquery.Client()

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

# table = client.get_table(table_id)  # Make an API request.
# print(
#     f"Loaded {table.num_rows} rows and {len(table.schema)} columns to {table_id}"
#     )



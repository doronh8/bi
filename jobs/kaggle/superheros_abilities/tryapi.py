import os
from kaggle.api.kaggle_api_extended import KaggleApi

# Define target path
target_path = os.path.expanduser('~/workspace/temp/data/bi/jobs/kaggle/superheros_abilities/')

# Make sure the target directory exists
os.makedirs(target_path, exist_ok=True)

# Set up the API
api = KaggleApi()
api.authenticate()

# Dataset identifier from Kaggle
dataset = 'hemajitpatel/superheros-abilities-dataset'

# Download and unzip the dataset into the target directory
api.dataset_download_files(dataset, path=target_path, unzip=True)

# List the downloaded files to verify
print("Files in target directory:", os.listdir(target_path))



"""temp
schema=[
        bigquery.SchemaField("Name", "STRING"),
        bigquery.SchemaField("Universe", "STRING"),
        bigquery.SchemaField("Alignment", "STRING"),
        bigquery.SchemaField("Strength", "INT64"),
        bigquery.SchemaField("Speed", "INT64"),
        bigquery.SchemaField("Intelligence", "INT64"),
        bigquery.SchemaField("Combat_skill", "INT64"),
        bigquery.SchemaField("Weapon", "STRING"),
        bigquery.SchemaField("Power_Score", "INT64"),
        bigquery.SchemaField("Popularity_Score", "INT64"),
    ],"""
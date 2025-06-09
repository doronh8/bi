# ETL - Extract Transform Load
## Definition of procedure

Last update 2025-01-03

## Goal - 
Develop ETL process which extracts data from Google Cloud Storage to Google Cloud BigQuery
`
## Methodology
Create a python script which execute all the steps and can be deployed to Virtual Machine - production

## Steps
1. Get permission to GCS
2. Explore the data in GCS
3. Extract sample data - Examine the schema, Which events. Developer docs
4. Transform - if needed
5. Load - Data to BigQuery
6. Validate the data in DWH
7. Develop script from A2Z in Python
8. Scheduling
9. Documentation
10. Logs & alerts
11. Configuration
12. Validation procedure

## Links
* [Google Cloud Storage - Public](https://console.cloud.google.com/storage/browser/cloud-samples-data/bigquery/us-states)
* [US states csv file](https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.csv)


## Operations
create jobs folder for the python scripts
```dtd
mkdir -p ./jobs/my_etl_02
touch ./jobs/my_etl_02/my_etl_02.py
```
add file header
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Free text


Reference


"""
```


create temp folder to save the logs and data file
```dtd
mkdir -p temp/data/bi/jobs/my_etl_01
mkdir -p temp/logs/bi/jobs/my_etl_01
```

[BigQuery UI](https://console.cloud.google.com/bigquery?)

Create dataset (Schema)<br>
Load the file to BigQuery - Manually
```dtd
create schema my_etl options (description ="My first ETL dataset") 
        
```



## Adjust operating system
```python
from pathlib import Path
import os

# adapt the env to mac or windows
if os.name == 'nt':
    home = Path("C:/workspace/")
else:
    home = Path(os.path.expanduser("~/workspace/"))


```
Read or Read File
```python
def readFile(fileName):
    with open(fileName, "r") as file:
        data = file.read()
        file.close()
    return data


def writeFile(fileName, Data):
    with open(fileName, "w", newline='', encoding='utf-8') as file:
        file.write(Data)
    file.close()

    
def readJsonFile(fileName):
    try:
        with open(fileName, "rb") as file:
            return json.load(file)
    except IOError as err:
        if err.errno == 2:  # File didn't exist, no biggie
            return {}
        else:  # Something weird, just re-raise the error
            raise

def header(string):
    x = len(string)*"="
    print(f"{string}\n{x}\n")

```

## Requests get
```python
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
if data:
    # print(json.dumps(data, indent=4))
    print(data)
```

Ensure Directory
```python
def ensureDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
```

[Load local file to BigQuery](https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-gcs-csv)


RegEx to extract folder name
```python
# adapt the env to mac or windows
home = Path(os.path.expanduser("C:" if os.name == "nt" else "~" ) + "/workspace/")

# get repository name
repo_name = re.search(r"(.*)[/\\]workspace[/\\]([^/\\]+)", __file__).group(2)
repo_tail = re.search(r".*[/\\]"+repo_name+r"[/\\](.+)[/\\]", __file__).group(1)
sys.path.insert(0, str(home / f"{repo_name}/utilities/"))
```

## Extract schema from table
```python
table_id = "ppltx-bi-developer.my_etl.us_states_json"
client = bigquery.Client()
table = client.get_table(table_id) 
client.schema_to_json(table.schema, "/Users/liadlivne/workspace/bidev/jobs/my_etl_05/config/us_states.json")
```


## Add External flags
```python
def process_command_line(argv):
    if argv is None:
        argv = sys.argv[1:]
    # initialize the parser object:

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("project_id", choices=["ppltx-ba-course", "ppltx-bi-developer"],
                        help="""Operation to perform. The arguments for each option are:
                        Full_Load:   --date""",
                        default="ppltx-ba-course")
    parser.add_argument("--etl-action", choices=["init", "daily", "delete"], help="""The action the etl job""")
    parser.add_argument("--etl-name", help="""The name of the etl job""")
    parser.add_argument("--dry-run", help="""if True don't execute the queries""", action="store_true")
    parser.add_argument("--days-back", help="""The number of days we want to go back""",
                        default=1)

    return parser, argparse.Namespace()


parser, flags = process_command_line(sys.argv[1:])
x = sys.argv[1:]
parser.parse_args(x, namespace=flags)
```
Parse the flags
```python
# define the project_id
project_id = flags.project_id
etl_name = flags.etl_name
etl_action = flags.etl_action
days_back = int(flags.days_back)
```
Get dates in python
```python
from datetime import datetime, timedelta, date

# Get dates
date_today = date.today()
y_m_d = (date_today + timedelta(days=-days_back)).strftime("%Y-%m-%d")
ymd = y_m_d.replace("-", "")
```

## Load additional files


## Bugs
Can not read local AVRO file
[Documentation](https://cloud.google.com/bigquery/docs/samples/bigquery-load-table-gcs-avro)
```python
  "us_states_avro": {
    "api_url": "https://storage.googleapis.com/cloud-samples-data/bigquery/us-states/us-states.avro",
    "data_file": "us-states.avro",
    "table_id": "ppltx-bi-developer.my_etl.us_states_avro",
    "SourceFormat": "AVRO"
  }
```




[Null Marker - Docs](https://cloud.google.com/bigquery/docs/reference/rest/v2/Job#JobConfigurationLoad.FIELDS.null_marker)


## Logs & Alerts
Monitor the ETL by its logs

### Add logs to the script
```python
step_id = 0
env_type = 'daily'
log_table = f"{project_id}.logs.daily_logs"

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



```

Log Format
```sql
SELECT 
  current_datetime() as ts,
  current_date() as dt,
  "39bc365d" as uid,
  "Liads-MBP-2.home" as username,
  "exec" as job_name,
  "daily" as job_type,
  "my_etl_07.py" as file_name,
  "end" as step_name,
  7 as step_id,
  "daily" as log_type,
  "free text" as message
```

## Scheduler file
Bash file which execute python commands in Virtual Machine
```commandline
#!/bin/bash

# Run the python script according to our configuration
cd ~/workspace/bidev/

# bash ~/workspace/bidev/jobs/my_etl_07/scheduler/execute_my_etl_daily.sh

python3 ./jobs/my_etl_07/my_etl_07.py  ppltx-bi-developer --etl-name animals --etl-action daily --dry-run


python3 ./jobs/my_etl_07/my_etl_07.py  ppltx-bi-developer --etl-name etl --etl-action daily
```


## Alerts types

1. Monitor logs
2. Monitor tables <br>
2.1 [Table alert query](https://cloud.google.com/bigquery/docs/information-schema-tables)<br>
2.2 [Table alert python - List tables](https://cloud.google.com/bigquery/docs/samples/bigquery-get-table)
3. Monitor KPIs

### Logs Alert Script - [Git Source](https://github.com/liadppltx/bidev/tree/main/jobs/my_etl_08)
1. Parse flags
2. Configuration - Get queries definition
3. Iterate all the queries
4. Sent notification if needed

Get Logs
```dtd
SELECT
  *
FROM
  `logs.daily_logs`
  order by ts desc
LIMIT
  1000
```

### Tables Alert - Query
```dtd
SELECT
  timestamp_diff(current_timestamp(),TIMESTAMP_MILLIS(last_modified_time ), hour) as df,
  TIMESTAMP_MILLIS(last_modified_time) last_modified,
  *
FROM
  logs.__TABLES__
```

### Tables Alert - Script client

get paths
```python
def get_paths(root, home, file_name, repo_tail):
    bi_path = home / f'{root}/'
    bi_auth = home / 'auth/'
    data_path = home / f'temp/data/{root}/{repo_tail}'
    logs_path = home / f'temp/logs/{root}/{repo_tail}'
    folder_name = Path(os.path.dirname(file_name))
    return bi_path, bi_auth, data_path, logs_path, folder_name
```
Time Zone issues
```python
run_time = datetime.now()
if not run_time.tzinfo:
    run_time = run_time.replace(tzinfo=timezone.utc)


if not table_modified.tzinfo:
    table_modified = table_modified.replace(tzinfo=timezone.utc)
tables_dict["hours_diff"].append(round((run_time - table_modified).total_seconds()/3600))

```
### KPIs Monitoring - Script
create random data for DAU using claude
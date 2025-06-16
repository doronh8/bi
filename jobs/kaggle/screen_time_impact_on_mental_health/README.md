# project

* project that includes config file - Done
* connected to source via api - Done
* clean data - Not needed
* add error exception
* 

[data source](https://www.kaggle.com/datasets/abhishekdave9/digital-habits-vs-mental-health-dataset)

# Notes
script is copied from previous project - superhero abilities.

# new project summary

* Load 100 rows initially at 08:00
* Then load 20 more rows at 16:00, 00:00, and again at 08:00 (next day), and repeat
* Maintain logs, alerts, KPIs, and track last update time
* Use BigQuery as destination
* Use Kaggle datasets as source

## chatGPT steps:

📊 Time-Driven Incremental ETL with Kaggle → BigQuery
🧩 Objective
Build a Python-based ETL that:

Loads 100 rows initially at 08:00       

Loads 20 more rows at 16:00, 00:00, and next 08:00

Supports logging, monitoring, and alerts

Loads data from Kaggle into BigQuery

🏗️ Architecture Overview
Feature	                        Tool/Method
ETL Logic	                    Python script (my_kaggle.py)
Scheduling	                    Google Cloud Scheduler
Execution Environment	        Cloud Functions / Cloud Run
Data Storage	                BigQuery
Logs	                        BigQuery Logging Table (logs.etl_kaggle_loads)
Metadata Tracking	            BigQuery Table (logs.etl_tracking)
Alerts/Monitoring	            Cloud Monitoring + Alert Policies

🛠️ ETL Command Line Flags
Use the --etl-action flag to control behavior:
```
bash
# Initial 100 rows
python my_kaggle.py --etl-name etl --etl-action init

# Incremental 20 rows
python my_kaggle.py --etl-name etl --etl-action step
```
🕒 Schedule via Google Cloud Scheduler

Time	--    Action	--    Rows Loaded

08:00	    init	    100

16:00	    step	    20

00:00	    step	    20

08:00	    step	    20

Create 3 Cloud Scheduler jobs that trigger your ETL with the right parameters.

🧠 Row Tracking Logic (Python)
Use BigQuery to track what was already loaded:

```
python
def get_last_loaded_row(table_id):
    query = f"""
    SELECT MAX(last_row_loaded) as last_row
    FROM `your_project.logs.etl_tracking`
    WHERE etl_name = '{etl_name}'
    """
    result = client.query(query).result()
    row = list(result)[0]
    return row.last_row or 0

start_row = get_last_loaded_row(table_id)
batch_size = 100 if flags.etl_action == "init" else 20
end_row = start_row + batch_size

df_batch = full_df.iloc[start_row:end_row]
df_batch.to_csv(temp_file, index=False)
```


Then insert a new record into logs.etl_tracking after a successful load.

📋 Logging and Metrics
Track each ETL run in a table like:
```
sql
Copy
Edit
logs.etl_kaggle_loads:
- timestamp
- etl_name
- rows_loaded
- status
- message
```
Track progress in:
```
sql
Copy
Edit
logs.etl_tracking:
- etl_name
- last_row_loaded
- total_loaded
- last_run_ts
```

🚨 Monitoring & Alerts
Set up alerts via Google Cloud Monitoring:

Create a log-based metric for "Load finished"

Alert if:

No new rows in 24h

Load failures occur

Total rows per day < expected

Send alerts via:

Email

Slack (via Pub/Sub + webhook)

SMS (via Google alerting)

✅ Summary
 * ETL handles init and step loads

 * Schedule jobs with Cloud Scheduler

 * Store progress in BigQuery tracking table

 * Monitor success and alert on failures

 * Scalable and cloud-native

Let me know if you want a pre-made Cloud Scheduler setup YAML or Terraform config for deployment.
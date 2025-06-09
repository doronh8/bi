# 1. BigQuery Scheduler
# scheduled_query

This is a task from the final project

## Description

Develop an ETL on public dataset.
Define its KPIs and scheduled it on:

1. BigQuery scheduler
2. Bash script - Which runs the query
3. Deploy to production on VM

## job description
the query will run on a daily basis and add 100 active users to the segmentation table.

## commands

```dtd
create schema fp_scheduled_query options(description="contains table of the daily segmentation")
```

## data treatment
data can also be used with truncate to replace the existing data

## scheduling
this job is scheduled by BigQuery to run every day at 08:00 UTC

## query link
```dtd
https://console.cloud.google.com/bigquery/scheduled-queries/locations/us/configs/6841c9b3-0000-2870-92b7-f403043d4cc4/runs?authuser=1&inv=1&invt=Abylpg&project=bi-course-461012
```


# 2. Bash Script

# CLI:
run with cli script <b>notice the ' < ' sign </b>
```dtd
#!/bin/bash
cd ppltx-tutorial/jobs/scheduled_query
bq query \
    --use_legacy_sql=false \
    < 'daily_list.sql'
```

# preview table
 <b>notice the ' : ' after projectID </b>
```dtd
bq head `bi-course-461012:fp_scheduled_query.daily_segment`
```

# if error with account and project 

choose account
```dtd
gcloud auth login
```

choose correct project with
```dtd
gcloud config set project YOUR_PROJECT_ID
```


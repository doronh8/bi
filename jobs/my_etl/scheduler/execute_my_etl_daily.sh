#!/bin/bash

# Exit on error
set -e

# Run the python script according to our configuration
cd ~/workspace/bi/

# bash ~/workspace/bi/jobs/my_etl/scheduler/execute_my_etl_daily.sh

python3 jobs/my_etl/my_etl.py  bi-course-461012 --etl-name animals --etl-action daily

python3 jobs/my_etl/my_etl.py  bi-course-461012 --etl-name etl --etl-action daily

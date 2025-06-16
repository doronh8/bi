#!/bin/bash

# Exit on error
set -e

# Run the python script according to our configuration
cd ~/workspace/

# bash ~/workspace/bi/jobs/my_etl/scheduler/execute_my_etl_daily.sh

python3 bi/jobs/kaggle/my_kaggle.py  bi-course-461012 bi-course-461012 --etl-action init --etl-name etl


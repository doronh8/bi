#!/bin/bash

# Exit on error
set -e

# Run the python script according to our configuration
#cd ~/workspace/bi/
cd "$HOME/workspace/bi"
# bash ~/workspace/bi/jobs/kaggle/scheduler/execute_my_kaggle_daily.sh
bash "$HOME/workspace/bi/jobs/kaggle/scheduler/execute_my_kaggle_daily.sh"

#python3 jobs/kaggle/my_kaggle.py  bi-course-461012 --etl-action step --etl-name etl
python3 jobs/kaggle/my_kaggle.py bi-course-461012 --etl-action step --etl-name etl



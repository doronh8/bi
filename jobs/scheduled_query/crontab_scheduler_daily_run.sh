#!/usr/bin/env bash

# Exit on error
set -e

# m h  dom mon dow   command
# 0 8 * * *   bash ~/workspace/ppltx-tutorial/jobs/scheduled_query/crontab_scheduler_daily_run.sh
# bash ~/workspace/ppltx-tutorial/jobs/scheduled_query/crontab_scheduler_daily_run.sh

#  ╔═══════════════════════════════════════════╗
#  ║    final project - Run daily segment      ║
#  ╚═══════════════════════════════════════════╝

cd ~/workspace/ppltx-tutorial/


bq query --use_legacy_sql=false < jobs/scheduled_query/daily_list.sql

#bq head -n=5 `bi-course-461012:fp_scheduled_query.daily_segment`
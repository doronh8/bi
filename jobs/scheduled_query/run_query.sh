#!/bin/bash

bq query \
    --use_legacy_sql=false \
    < 'daily_list.sql'
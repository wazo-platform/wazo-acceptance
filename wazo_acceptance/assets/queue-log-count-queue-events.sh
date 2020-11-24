#!/bin/bash

queue_name=$1
event_name=$2

sudo -u postgres psql asterisk --no-align --tuples-only -c "select count(*) from queue_log where queuename = '$queue_name' and event = '$event_name'"

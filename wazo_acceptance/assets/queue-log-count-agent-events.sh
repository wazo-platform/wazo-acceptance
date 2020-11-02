#!/bin/bash

agent_number=$1
event_name=$2

sudo -u postgres psql asterisk --no-align --tuples-only -c "select count(*) from queue_log where agent = 'Agent/$agent_number' and event = '$event_name'"

#!/bin/bash

queue_name=$1

sudo -u postgres psql asterisk -c "delete from queue_log where queuename = '$queue_name'"

#!/bin/bash

queue_name=$1

sudo -u postgres psql asterisk -c "delete from queue_log where queuename = '$queue_name'"
sudo -u postgres psql asterisk -c "delete from stat_queue_periodic where stat_queue_id in (select id from stat_queue where name = '$queue_name')"
sudo -u postgres psql asterisk -c "delete from stat_call_on_queue where stat_queue_id in (select id from stat_queue where name = '$queue_name')"
sudo -u postgres psql asterisk -c "delete from stat_queue where name = '$queue_name'"

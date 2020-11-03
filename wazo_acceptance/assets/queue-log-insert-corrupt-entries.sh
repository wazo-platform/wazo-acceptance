#!/bin/bash

sudo -u postgres psql asterisk -c "INSERT INTO queue_log(time, callid, queuename, agent, event, data1) VALUES (localtimestamp - interval '1 hour', 'test_exitwithtimeout', 'q1', 'NONE', 'EXITWITHTIMEOUT', '1')"

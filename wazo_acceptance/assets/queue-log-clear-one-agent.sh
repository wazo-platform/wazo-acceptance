#!/bin/bash

agent_number=$1

sudo -u postgres psql asterisk -c "delete from queue_log where agent = 'Agent/$agent_number'"

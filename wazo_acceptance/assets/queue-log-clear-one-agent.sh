#!/bin/bash

agent_number=$1

sudo -u postgres psql asterisk -c "delete from queue_log where agent = 'Agent/$agent_number'"
sudo -u postgres psql asterisk -c "delete from stat_agent_periodic where stat_agent_id in (select id from stat_agent where name = 'Agent/$agent_number')"
sudo -u postgres psql asterisk -c "delete from stat_call_on_queue where stat_agent_id in (select id from stat_agent where name = 'Agent/$agent_number')"
sudo -u postgres psql asterisk -c "delete from stat_agent where name = 'Agent/$agent_number'"
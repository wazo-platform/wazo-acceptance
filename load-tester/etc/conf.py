# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

## global configuration

sipp_remote_host = 'skaro-load'

sipp_local_ip = '192.168.32.241'
sipp_call_rate = 1.0
sipp_pause_in_ms = 1000
sipp_rate_period_in_ms = 1000

## scenarios configuration

called_line = {
    'username': 'xto5ow',
    'bind_port': 5060,
}

calling_line = {
    'username': 'po7pit',
    'password': 'JRPUZS',
}

#scenarios.call_and_answer_call.calling_line = calling_line
#scenarios.call_and_answer_call.called_line = called_line
scenarios.call_and_answer_call.called_exten = '1002'

#scenarios.call_then_hangup.calling_line = calling_line
scenarios.call_then_hangup.called_exten = '1'

#scenarios.call_then_wait.calling_line = calling_line
scenarios.call_then_wait.called_exten = '1'

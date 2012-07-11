# -*- coding: UTF-8 -*-

from __future__ import unicode_literals

sipp_remote_host = 'skarodev'

sipp_local_ip = '10.39.0.254'
sipp_call_rate = 1.0
sipp_rate_period_in_ms = 1000

calling_line_call_then_wait = {
    'username': 'call_then_wait',
    'password': 'call_then_wait',
}

scenarios.call_then_wait.calling_line = calling_line_call_then_wait
scenarios.call_then_wait.sipp_nb_of_calls_before_exit = 3
scenarios.call_then_wait.called_extens = ['5200']
scenarios.call_then_wait.pause = {'distribution': 'fixed', 'value': 1000}

calling_line_call_then_hangup = {
    'username': 'call_then_hangup',
    'password': 'call_then_hangup',
}

scenarios.call_then_hangup.calling_line = calling_line_call_then_hangup
scenarios.call_then_hangup.sipp_nb_of_calls_before_exit = 1
scenarios.call_then_hangup.called_extens = ['5200']
scenarios.call_then_hangup.pause = {'distribution': 'fixed', 'value': 10000}

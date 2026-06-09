# Copyright 2026 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given, then, when
from wazo_test_helpers import until

from .. import auth_worker

# Hit wazo-auth directly (not through nginx, whose upstream keep-alive would
# pin requests to a single instance and hide the SO_REUSEPORT load-balancing).
LOCAL_AUTH_URL = 'http://127.0.0.1:9497/0.1/backends'
REMOVER_LOG = 'ExpiredTokenRemover took'


@given('an HTTP worker is running')
def given_an_http_worker_is_running(context):
    if not auth_worker.is_available(context):
        context.scenario.skip('wazo-auth does not ship the HTTP worker unit')
        return
    assert auth_worker.is_active(context), 'the HTTP worker is not running'


@when('I send {count:d} requests to the local auth API')
def when_i_send_requests_to_local_auth(context, count):
    context.worker_requests_since = context.ssh_client.out_call(['date', '+%s']).strip()
    burst = (
        f'for i in $(seq {count}); do '
        f'curl -s -o /dev/null -H "Connection: close" {LOCAL_AUTH_URL}; done'
    )
    context.ssh_client.check_call([burst])


@then('the HTTP worker served at least one request')
def then_the_worker_served_a_request(context):
    since = context.worker_requests_since

    def _worker_logged_request():
        logs = context.ssh_client.out_call(
            [f'journalctl --no-pager -u {auth_worker.WORKER_INSTANCE} --since=@{since}']
        )
        return '/0.1/backends' in logs

    until.true(
        _worker_logged_request,
        tries=15,
        message='the HTTP worker never served a request',
    )


@then('the HTTP worker does not run the expired-token remover')
def then_worker_does_not_run_remover(context):
    logs = context.ssh_client.out_call(
        [f'journalctl --no-pager -u {auth_worker.WORKER_INSTANCE}']
    )
    assert REMOVER_LOG not in logs, 'the HTTP worker must not run the ExpiredTokenRemover'

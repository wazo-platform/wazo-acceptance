# -*- coding: UTF-8 -*-

from lettuce.decorators import step
from xivo_lettuce import sysutils, logs

@step(u'When I try to log in agent "([^"]*)" with extension "([^"]*)" through xivoagentctl')
def when_i_try_to_log_in_agent_through_xivoagentctl(step, agent, extension):
    number, context = extension.split('@')
    command = ['xivo-agentctl', '-c', '"login %s %s %s"' % (agent, number, context)]
    sysutils.send_command(command, False)


@step(u'When I try to log off agent "([^"]*)" through xivoagentctl')
def when_i_try_to_log_off_agent_through_xivoagentctl(step, agent):
    command = ['xivo-agentctl', '-c', '"logoff %s"' % agent]
    sysutils.send_command(command, False)

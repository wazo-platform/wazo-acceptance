# -*- coding: UTF-8 -*-

from lettuce import step
from xivo_lettuce import sysutils, logs


@step(u'When I restart Asterisk')
def when_i_restart_asterisk(step):
    command = ['service', 'asterisk', 'restart']
    sysutils.send_command(command)


@step(u'When I try to log in agent "([^"]*)" with extension "([^"]*)" through xivo-agentctl')
def when_i_try_to_log_in_agent_through_xivoagentctl(step, agent, extension):
    number, context = extension.split('@')
    command = ['xivo-agentctl', '-c', '"login %s %s %s"' % (agent, number, context)]
    sysutils.send_command(command)


@step(u'When I try to log off agent "([^"]*)" through xivo-agentctl')
def when_i_try_to_log_off_agent_through_xivoagentctl(step, agent):
    command = ['xivo-agentctl', '-c', '"logoff %s"' % agent]
    sysutils.send_command(command)


@step(u'Then I see that xivo-agent has reconnected to the AMI in the logs')
def then_i_see_that_xivo_agent_has_reconnected_to_the_ami_in_the_logs(step):
    logs.search_str_in_xivo_agent_log("Connecting AMI client to localhost:5038")

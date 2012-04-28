from lettuce.decorators import step
from lettuce.registry import world

from xivo_lettuce.manager import agent_manager

@step(u'Given there is an agent "([^"]*)" with number "([^"]*)"')
def given_there_is_an_agent_1_with_number_2(step, firstname, number):
    agent_manager.delete_agent(number)
    agent_manager.insert_agent(firstname, '', number, '')

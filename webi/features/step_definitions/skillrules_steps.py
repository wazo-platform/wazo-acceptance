from lettuce.decorators import step
from xivo_lettuce.manager import skill_rule_manager


@step(u'Given I remove skill rule "([^"]*)"')
def given_i_remove_skill_rule(step, skill_rule_name):
    skill_rule_manager.delete(skill_rule_name)

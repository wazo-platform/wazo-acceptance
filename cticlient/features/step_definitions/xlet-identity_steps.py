from webi.features.step_definitions.user_steps import *
from webi.features.step_definitions.voicemail_steps import *
from webi.features.step_definitions.line_steps import *

CONFIG_URL = '/xivo/configuration/index.php'

@step(u'Given I go to the "([^"]*)" configuration page')
def given_i_go_to_the_1_configuration_page(step, section_name):
    world.browser.get('%s%s' % (world.url, CONFIG_URL))
    link = world.browser.find_element_by_link_text(section_name)
    link.click()


@step(u'Given I read the field "([^"]*)"')
def given_i_read_the_field_group1(step, field_label):
    input_field = world.browser.find_element_by_label(field_label)
    world.stocked_infos[field_label] = input_field.text


@step(u'Then the Xlet identity shows name as "([^"]*)" "([^"]*)"')
@xivoclient_step
def then_the_xlet_identity_shows_name_as_1_2(step, firstname, lastname):
    assert world.xc_response == 'OK'


@step(u'Then the Xlet identity shows server name as field "([^"]*)"')
def then_the_xlet_identity_shows_server_name_as_field_1(step, field_label):
    @xivoclient
    def then_the_xlet_identity_shows_server_name_as_field_1_modified(field_value):
        pass
    field_value = world.stocked_infos[field_label]
    then_the_xlet_identity_shows_server_name_as_field_1_modified(field_value)
    assert world.xc_response == 'OK'


@step(u'Then the Xlet identity shows phone number as "([^"]*)"')
@xivoclient_step
def then_the_xlet_identity_shows_phone_number_as_1(step, linenumber):
    assert world.xc_response == 'OK'


@step(u'Then the Xlet identity shows a voicemail "([^"]*)"')
@xivoclient_step
def then_the_xlet_identity_shows_a_voicemail_1(step, vm_number):
    assert world.xc_response == 'OK'

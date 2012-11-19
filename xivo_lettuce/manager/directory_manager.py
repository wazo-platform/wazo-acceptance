from lettuce import world
from xivo_lettuce.form import submit, input, select
from xivo_lettuce.common import open_url
import time

def create_directory(directory):
    open_url('directory_config', 'add')
    input.set_text_field_with_label("Directory name", directory['name'])
    input.set_text_field_with_label("URI", directory['URI'])
    select.set_select_field_with_label("Type", directory['type'])
    submit.submit_form()


def add_directory_definition(directory):
    open_url('cti_directory', 'add')
    input.set_text_field_with_label("Name", directory['name'])
    input.set_text_field_with_label("Delimiter", directory['delimiter'])
    input.set_text_field_with_label("Direct match", directory['direct match'])
    select.set_select_field_with_label("URI", directory['URI'])


def add_field(fieldname, value):
    b = world.browser
    add_btn = b.find_element_by_css_selector(".sb-list table .sb-top .th-right a")
    add_btn.click()

    xpath = "//div[@class='sb-list']/table[position()=1]/tbody/tr[last()]/td[position()=%s]/input"
    fieldname_input = b.find_element_by_xpath(xpath % 1)
    fieldname_input.send_keys(fieldname)

    value_input = b.find_element_by_xpath(xpath % 2)
    value_input.send_keys(value)


def add_directory_to_context(directory):
    select.set_select_field_with_id("it-directorieslist", directory)

    right_arrow = world.browser.find_element_by_xpath("//div[@class='inout-list']/a[position()=1]")
    right_arrow.click()



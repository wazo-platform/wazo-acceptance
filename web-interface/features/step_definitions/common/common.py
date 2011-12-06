# -*- coding: utf-8 -*-

from lettuce.registry import world
from selenium.common.exceptions import NoSuchElementException

from checkbox import Checkbox

class FormErrorException (Exception):
    pass

def the_option_is_checked(option_label, checkstate, **kwargs):
    """Reads or write the value of a checkbox, selected by its label text.
       Use given = True if you want to set the checkbox"""
    # If given, then we set the option.
    # If not given, we assert the option is in checkstate.
    if 'given' in kwargs:
        given = kwargs['given']
    else:
        given = False

    # Get the webelement.
    world.last_option_label = option_label
    option = world.browser.find_element_by_label(option_label)

    # Determine the action to do.
    goal_checked = (checkstate is None)
    if not given:
        assert Checkbox(option).is_checked() == goal_checked
    else:
        Checkbox(option).set_checked(goal_checked)
        submit_form()

def find_form_errors():
    """Find the box containing form errors."""
    return world.browser.find_element_by_id('report-xivo-error')

def submit_form():
    """Every (?) submit button in the Webi has the same id."""
    submit_button = world.browser.find_element_by_id('it-submit')
    submit_button.click()
    try:
        error_element = find_form_errors()
    except NoSuchElementException:
        return
    raise FormErrorException(error_element.text)

def find_line(line_substring):
    """Return the tr webelement of a list table."""
    return world.browser.find_element_by_xpath(
        "//table[@id='table-main-listing']//tr[contains(.,'%s')]" % line_substring)

def remove_line(line_substring):
    """Remove a line in a list table."""
    table_line = find_line(line_substring)
    delete_button = table_line.find_element_by_xpath(".//a[@title='Delete']")
    delete_button.click()
    alert = world.browser.switch_to_alert();
    alert.accept()

def edit_line(line_substring):
    """Edit an element of a list table."""
    table_line = find_line(line_substring)
    edit_button = table_line.find_element_by_xpath(".//a[@title='Edit']")
    edit_button.click()

def go_to_tab(tab_label):
    """Click a tab button."""
    tab_button = world.browser.find_element_by_xpath(
        "//div[@class='tab']//a[contains(.,'%s')]" % tab_label)
    tab_button.click()

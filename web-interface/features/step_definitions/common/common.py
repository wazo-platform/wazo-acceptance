# -*- coding: utf-8 -*-

from lettuce.registry import world

from checkbox import Checkbox

def find_element_by_label(label):
    '''Finds the first element corresponding to the label containing the argument'''
    webelement_label = world.browser.find_element_by_xpath("//label[contains(.,'%s')]" % label)
    webelement_id = webelement_label.get_attribute('for')
    webelement = world.browser.find_element_by_id(webelement_id)
    return webelement

def find_elements_by_label(label):
    '''Finds all elements corresponding to the labels containing the argument'''
    webelement_labels = world.browser.find_elements_by_xpath("//label[contains(.,'%s')]" % label)
    ret = []
    for webelement_label in webelement_labels:
        webelement_id = webelement_label.get_attribute('for')
        ret += world.browser.find_elements_by_id(webelement_id)
    return ret

def the_option_is_checked(option_label, checkstate, **kwargs):
    '''Reads or write the value of a checkbox, selected by its label text.
       Use given = True if you want to set the checkbox'''
    # If given, then we set the option.
    # If not given, we assert the option is in checkstate.
    if 'given' in kwargs:
        given = kwargs['given']
    else:
        given = False

    # Get the webelement.
    world.last_option_label = option_label
    option = find_element_by_label(option_label)

    # Determine the action to do.
    goal_checked = (checkstate is None)
    if not given:
        assert Checkbox(option).is_checked() == goal_checked
    else:
        Checkbox(option).set_checked(goal_checked)
        submit_form()

def submit_form():
    '''Every (?) submit button in the Webi has the same id'''
    submit_button = world.browser.find_element_by_id('it-submit')
    submit_button.click()

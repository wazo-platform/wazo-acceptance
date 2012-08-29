# -*- coding: utf-8 -*-

from lettuce.registry import world


def type_name(name):
    world.browser.find_element_by_id('it-meetmefeatures-name', 'Meetme form not loaded')
    input_name = world.browser.find_element_by_id('it-meetmefeatures-name')
    input_name.clear()
    input_name.send_keys(name)


def type_confno(confno):
    world.browser.find_element_by_id('it-meetmefeatures-confno', 'Meetme form not loaded')
    input_confno = world.browser.find_element_by_id('it-meetmefeatures-confno')
    input_confno.clear()
    input_confno.send_keys(confno)


def type_context(context):
    world.browser.find_element_by_id('it-meetmefeatures-context', 'Meetme form not loaded')
    language_option = world.browser.find_element_by_xpath('//select[@id="it-meetmefeatures-context"]//option[@value="%s"]' % context)
    language_option.click()


def type_maxusers(maxusers):
    world.browser.find_element_by_id('it-meetmefeatures-maxusers', 'Meetme form not loaded')
    input_maxusers = world.browser.find_element_by_id('it-meetmefeatures-maxusers')
    input_maxusers.clear()
    input_maxusers.send_keys(maxusers)

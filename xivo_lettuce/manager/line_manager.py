# -*- coding: utf-8 -*-


from lettuce.registry import world


def delete_line_from_number(number, context):
    for id in find_line_id_from_number(number, context):
        world.ws.lines.delete(id)


def find_line_id_from_number(number, context):
    lines = world.ws.lines.search_by_number(number)
    if lines:
        return [line.id for line in lines if
                line.number == str(number) and line.context == str(context)]
    return []


def search_line_number(line_number):
    open_url('line')
    searchbox_id= 'it-toolbar-search'
    text_input = world.browser.find_element_by_id(searchbox_id)
    text_input.clear()
    text_input.send_keys(line_number)
    submit_button = world.browser.find_element_by_id('it-toolbar-subsearch')
    submit_button.click()


def unsearch_line():
    open_url('line')
    searchbox_id = 'it-toolbar-search'
    text_input = world.browser.find_element_by_id(searchbox_id)
    text_input.clear()
    submit_button = world.browser.find_element_by_id('it-toolbar-subsearch')
    submit_button.click()

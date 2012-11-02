# -*- coding: UTF-8 -*-

from lettuce.registry import world


def set_text_field_with_label(field_label, value):
    text_input = world.browser.find_element_by_label(field_label)
    text_input.clear()
    text_input.send_keys(value)


def set_text_field_with_id(field_id, value):
    text_input = world.browser.find_element_by_id(field_id)
    text_input.clear()
    text_input.send_keys(value)


def edit_text_field_with_id(field_id, new_value):
    input_field = world.browser.find_element_by_id(field_id)
    input_field.clear()
    input_field.send_keys(new_value)

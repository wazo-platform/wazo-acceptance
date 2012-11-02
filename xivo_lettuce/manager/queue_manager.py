# -*- coding: utf-8 -*-

from xivo_lettuce.manager_ws import queue_manager_ws, context_manager_ws
from xivo_lettuce import form


def remove_queues_with_name_or_number_if_exist(queue_name, queue_number):
    queue_manager_ws.delete_queues_with_name(queue_name)
    queue_manager_ws.delete_queues_with_number(queue_number)


def type_queue_name_display_name_number_context(name, display_name, extension, context):
    form.input.set_text_field_with_label('Name', name)
    form.input.set_text_field_with_label('Display name', display_name)
    form.input.set_text_field_with_label('Number', extension)
    context = context_manager_ws.get_context_with_name(context)
    context_field_value = '%s (%s)' % (context.display_name, context.name)
    form.select.set_select_field_with_label('Context', context_field_value)


def type_queue_ring_strategy(ring_strategy):
    form.select.set_select_field_with_label('Ring strategy', ring_strategy)

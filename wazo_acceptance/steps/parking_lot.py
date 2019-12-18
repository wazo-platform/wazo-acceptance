# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from behave import given


@given('there are parking lots with infos')
def given_there_are_parking_lots_with_infos(context):
    context.table.require_columns(['name', 'exten', 'context'])
    for row in context.table:
        body = row.as_dict()
        parking_lot = context.helpers.parking_lot.create(body)

        extension_body = {'exten': body['exten'], 'context': body['context']}
        extension = context.helpers.extension.create(extension_body)
        context.helpers.parking_lot.add_extension(parking_lot, extension)

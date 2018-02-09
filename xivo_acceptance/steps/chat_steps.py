# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from lettuce.decorators import step
from lettuce.registry import world

from xivo_acceptance.helpers import user_helper


@step(u'When I publish a chat message:')
def when_i_publish_a_chat_message(step):
    data = step.hashes[0]
    user_uuid = user_helper.get_by_firstname_lastname(data['firstname'], data['lastname'])['uuid']
    world.ctid_ng_client.chats.send_message(data['from'], user_uuid, data['alias'], data['msg'])

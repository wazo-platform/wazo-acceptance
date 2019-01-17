# -*- coding: utf-8 -*-
# Copyright (C) 2013-2016 Avencall
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from lettuce import step

from xivo_acceptance.helpers import extension_helper


@step(u'Given I have no extension with exten "([^"]*)"')
def given_i_have_no_extension_with_exten_group1(step, pattern):
    exten, context = pattern.split('@')
    extension = extension_helper.find_extension_by_exten_context(exten, context)
    if extension:
        extension_helper.delete_extension(extension['id'])


@step(u'Given I have the following extensions:')
def given_i_have_the_following_extensions(step):
    for exteninfo in step.hashes:
        extension = _extract_extension_parameters(exteninfo)
        extension_helper.add_or_replace_extension(extension)


def _extract_extension_parameters(parameters):

    if 'id' in parameters:
        parameters['id'] = int(parameters['id'])

    if 'commented' in parameters:
        parameters['commented'] = (parameters['commented'] == 'true')

    return parameters

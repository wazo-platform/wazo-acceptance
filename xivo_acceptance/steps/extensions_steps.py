# -*- coding: utf-8 -*-

# Copyright (C) 2013-2016 Avencall
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from hamcrest import assert_that
from hamcrest import has_entries
from hamcrest import has_key
from hamcrest import has_items
from hamcrest import is_not
from lettuce import step, world

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


@step(u'Then I get a list containing the following extensions:')
def then_i_get_a_list_containing_the_following_extensions(step):
    expected_extensions = step.hashes
    extensions = _filter_out_default_extensions()

    entries = [has_entries(e) for e in expected_extensions]
    assert_that(extensions, has_items(*entries))


@step(u'Then I get a list that does not contain the following extensions:')
def then_i_get_a_list_that_does_not_contain_the_following_extensions(step):
    expected_extensions = step.hashes
    extensions = _filter_out_default_extensions()

    entries = [has_entries(e) for e in expected_extensions]
    assert_that(extensions, is_not(has_items(*entries)))


@step(u'Then I have an extension with the following parameters:')
def then_i_have_an_extension_with_the_following_parameters(step):
    parameters = _extract_extension_parameters(step.hashes[0])
    extension = world.response.data

    assert_that(extension, has_entries(parameters))


def _filter_out_default_extensions():
    assert_that(world.response.data, has_key('items'))
    extensions = [e for e in world.response.data['items'] if e['context'] != 'xivo-features']
    return extensions


def _extract_extension_parameters(parameters):

    if 'id' in parameters:
        parameters['id'] = int(parameters['id'])

    if 'commented' in parameters:
        parameters['commented'] = (parameters['commented'] == 'true')

    return parameters

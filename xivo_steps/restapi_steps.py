# -*- coding: utf-8 -*-

# Copyright (C) 2013 Avencall
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


from lettuce import step
from xivo_lettuce.manager import restapi_requests_manager


@step(u'Then the REST API received a request with infos:$')
def then_the_rest_api_received_a_request_with_infos(step):
    for request_infos in step.hashes:
        restapi_requests_manager.assert_last_request_matches(**request_infos)

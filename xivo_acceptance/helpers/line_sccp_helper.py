# -*- coding: utf-8 -*-

# Copyright (C) 2015 Avencall
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

from xivo_acceptance.lettuce import postgres


def delete_line(line_id):
    query = """
    DELETE FROM
        sccpdevice
    WHERE
        line = (
            SELECT
                sccpdevice.name
            FROM
                linefeatures
                INNER JOIN sccpdevice
                    ON sccpdevice.id = linefeatures.protocolid
                    AND linefeatures.protocol = 'sccp'
            WHERE
                linefeatures.id = :line_id
            )
    """
    postgres.exec_sql_request(query, line_id=line_id)

    query = """
    DELETE FROM
        sccpline
    WHERE
        sccpline.id = (
            SELECT
                protocolid
            FROM
                linefeatures
            WHERE
                id = :line_id
        )
    """
    postgres.exec_sql_request(query, line_id=line_id)

    query = """
    DELETE FROM
        linefeatures
    WHERE
        id = :line_id
    """
    postgres.exec_sql_request(query, line_id=line_id)

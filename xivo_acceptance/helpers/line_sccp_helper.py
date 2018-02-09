# -*- coding: utf-8 -*-
# Copyright (C) 2015 Avencall
# SPDX-License-Identifier: GPL-3.0+

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


def find_all_line_ids_by_exten(exten):
    query = """
    SELECT
        linefeatures.id
    FROM
        linefeatures
        INNER JOIN sccpline
            ON linefeatures.protocolid = sccpline.id
            AND linefeatures.protocol = 'sccp'
    WHERE
        sccpline.name = :exten
    """
    result = postgres.exec_sql_request(query, exten=exten)
    return [row['id'] for row in result]

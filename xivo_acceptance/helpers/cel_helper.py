# -*- coding: utf-8 -*-
# Copyright 2013-2018 The Wazo Authors  (see the AUTHORS file)
# Copyright (C) 2016 Proformatique Inc.
# SPDX-License-Identifier: GPL-3.0-or-later

from xivo_acceptance.lettuce import postgres


def delete_all():
    query = "DELETE FROM cel"
    postgres.exec_sql_request(query)


def insert_entries(entries):
    for entry in entries:
        cel = dict(entry)

        for key in ['userdeftype', 'cid_ani', 'cid_rdnis', 'cid_dnid', 'channame', 'appname', 'appdata', 'accountcode', 'peeraccount', 'peer', 'userfield']:
            cel.setdefault(key, '')

        cel.setdefault('amaflags', 0)
        if 'call_log_id' in cel and cel['call_log_id']:
            cel['call_log_id'] = int(cel['call_log_id'])
        else:
            cel['call_log_id'] = None

        query = """INSERT INTO cel VALUES (
                      {id},
                      :eventtype,
                      :eventtime,
                      :userdeftype,
                      :cid_name,
                      :cid_num,
                      :cid_ani,
                      :cid_rdnis,
                      :cid_dnid,
                      :exten,
                      :context,
                      :channame,
                      :appname,
                      :appdata,
                      :amaflags,
                      :accountcode,
                      :peeraccount,
                      :uniqueid,
                      :linkedid,
                      :userfield,
                      :peer,
                      :call_log_id
                      )""".format(id=':id' if 'id' in cel else 'DEFAULT')

        postgres.exec_sql_request(query, **cel)

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

ALIAS = {
    'recording file': {
        'module': 'sounds',
        'qry': {'dir': 'recordings'}
    },
    'recording meetme file': {
        'module': 'sounds',
        'qry': {'dir': 'recordings-meetme'}
    },
    'musiconhold file': {
        'module': 'musiconhold',
        'qry': {'act': 'listfile',
                'cat': 'default'}
    },
    'agent group': {
        'module': 'agent'
    },
    'SIP line': {
        'module': 'line'
    },
    'LDAP server': {
        'module': 'ldapserver'
    },
    'LDAP filter': {
        'module': 'ldapfilter'
    },
    'CTI profile': {
        'module': 'profile'
    },
}

URLS = {
    'user': '/service/ipbx/index.php/pbx_settings/users',
    'group': '/service/ipbx/index.php/pbx_settings/groups',
    'line': '/service/ipbx/index.php/pbx_settings/lines',
    'device': '/service/ipbx/index.php/pbx_settings/devices',
    'voicemail': '/service/ipbx/index.php/pbx_settings/voicemail',
    'meetme': '/service/ipbx/index.php/pbx_settings/meetme',
    'context': '/service/ipbx/index.php/system_management/context',
    'configfiles': '/service/ipbx/index.php/system_management/configfiles',
    'general_iax': '/service/ipbx/index.php/general_settings/iax',
    'general_sip': '/service/ipbx/index.php/general_settings/sip',
    'incall': '/service/ipbx/index.php/call_management/incall',
    'outcall': '/service/ipbx/index.php/call_management/outcall',
    'cel': '/service/ipbx/index.php/call_management/cel',
    'callfilter': '/service/ipbx/index.php/call_management/callfilter',
    'trunkcustom': '/service/ipbx/index.php/trunk_management/custom',
    'trunksip': '/service/ipbx/index.php/trunk_management/sip',
    'trunkiax': '/service/ipbx/index.php/trunk_management/iax',
    'sounds': '/service/ipbx/index.php/pbx_services/sounds',
    'musiconhold': '/service/ipbx/index.php/pbx_services/musiconhold',
    'extenfeatures': '/service/ipbx/index.php/pbx_services/extenfeatures',
    'provd_general': '/xivo/configuration/index.php/provisioning/general',
    'provd_plugin': '/xivo/configuration/index.php/provisioning/plugin',
    'queue': '/callcenter/index.php/settings/queues',
    'agent': '/callcenter/index.php/settings/agents',
    'skill_rule': '/callcenter/index.php/settings/queueskillrules',
    'profile': '/cti/index.php/profiles',
    'ldapserver': '/xivo/configuration/index.php/manage/ldapserver',
    'ldapfilter': '/service/ipbx/index.php/system_management/ldapfilter',
    'backups': '/service/ipbx/index.php/system_management/backupfiles',
    'certificat': '/xivo/configuration/index.php/manage/certificate',
    'dhcp': '/xivo/configuration/index.php/network/dhcp',
    'sheet': 'cti/index.php/sheetactions/',
    'sheetevent': 'cti/index.php/sheetevents/',
    'sccpgeneralsettings': '/service/ipbx/index.php/general_settings/sccp',
    'general_settings': '/xivo/configuration/index.php/manage/general',
    'phonebook': '/service/ipbx/index.php/pbx_services/phonebook',
    'phonebook_settings': '/service/ipbx/index.php/general_settings/phonebook',
    'parking': '/service/ipbx/index.php/pbx_services/extenfeatures/#parking',
    'directory_config': '/xivo/configuration/index.php/manage/directories',
    'cti_directory': '/cti/index.php/directories',
    'cti_direct_directory': '/cti/index.php/contexts',
    'cti_display_filter': '/cti/index.php/displays',
    'admin_user': '/xivo/configuration/index.php/manage/user',
    'schedule': '/service/ipbx/index.php/call_management/schedule',
}

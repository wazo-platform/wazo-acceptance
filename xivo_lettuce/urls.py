# -*- coding: utf-8 -*-

ALIAS = {
         'recording file':
             {
              'module': 'sounds',
              'qry': {'dir': 'recordings'}
             },
         'musiconhold file':
             {
              'module': 'musiconhold',
              'qry': {'act': 'listfile',
                      'cat': 'default'}
             },
         'SIP line':
             {
              'module': 'line'
             },
         'LDAP server':
             {
              'module': 'ldapserver'
             },
         'LDAP filter':
             {
              'module': 'ldapfilter'
             }
        }

URLS = {
        'user': 
            {
                'web': '/service/ipbx/index.php/pbx_settings/users',
                'ws': 'ipbx/pbx_settings/users'
            },
        'group': 
            {
                'web': '/service/ipbx/index.php/pbx_settings/groups',
                'ws': 'ipbx/pbx_settings/groups'
            },
        'line': 
            {
                'web': '/service/ipbx/index.php/pbx_settings/lines',
                'ws': 'ipbx/pbx_settings/lines'
            },
        'voicemail': 
            {
                'web': '/service/ipbx/index.php/pbx_settings/voicemail',
                'ws': 'ipbx/pbx_settings/voicemail'
            },
        'meetme': 
            {
                'web': '/service/ipbx/index.php/pbx_settings/meetme',
                'ws': 'ipbx/pbx_settings/meetme'
            },
        'context': 
            {
                'web': '/service/ipbx/index.php/system_management/context',
                'ws': 'ipbx/system_management/context'
            },
        'configfiles': 
            {
                'web': '/service/ipbx/index.php/system_management/configfiles',
                'ws': None
            },
        'general_iax': 
            {
                'web': '/service/ipbx/index.php/general_settings/iax',
                'ws': 'ipbx/general_settings/iax'
            },
        'incall': 
            {
                'web': '/service/ipbx/index.php/call_management/incall',
                'ws': 'ipbx/call_management/incall'
            },
        'outcall': 
            {
                'web': '/service/ipbx/index.php/call_management/outcall',
                'ws': 'ipbx/call_management/outcall'
            },
        'trunkcustom': 
            {
                'web': '/service/ipbx/index.php/trunk_management/custom',
                'ws': 'ipbx/trunk_management/custom'
            },
        'trunksip': 
            {
                'web': '/service/ipbx/index.php/trunk_management/sip',
                'ws': 'ipbx/trunk_management/sip'
            },
        'trunkiax': 
            {
                'web': '/service/ipbx/index.php/trunk_management/iax',
                'ws': 'ipbx/trunk_management/iax'
            },
        'sounds': 
            {
                'web': '/service/ipbx/index.php/pbx_services/sounds',
                'ws': 'ipbx/pbx_services/sounds'
            },
        'musiconhold': 
            {
                'web': '/service/ipbx/index.php/pbx_services/musiconhold',
                'ws': None
            },
        'provd_general': 
            {
                'web': '/xivo/configuration/index.php/provisioning/general',
                'ws': 'configuration/provisioning/general'
            },
        'provd_plugin': 
            {
                'web': '/xivo/configuration/index.php/provisioning/plugin',
                'ws': None
            },
        'queue': 
            {
                'web': '/callcenter/index.php/settings/queues',
                'ws': 'callcenter/settings/queues'
            },
        'agent': 
            {
                'web': '/callcenter/index.php/settings/agents',
                'ws': 'callcenter/settings/agents'
            },
        'profile': 
            {
                'web': '/cti/index.php/profiles',
                'ws': None
            },
        'ldapserver': 
            {
                'web': '/xivo/configuration/index.php/manage/ldapserver',
                'ws': None
            },
        'ldapfilter': 
            {
                'web': '/service/ipbx/index.php/system_management/ldapfilter',
                'ws': None
            },
       }

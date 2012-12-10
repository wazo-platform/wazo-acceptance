

\connect xivo;

BEGIN;

truncate accesswebservice;
INSERT INTO accesswebservice VALUES (DEFAULT,'test','admin','proformatique','','a:1:{s:3:"acl";a:4:{s:4:"xivo";a:1:{s:13:"configuration";a:5:{s:5:"check";b:1;s:6:"manage";a:1:{s:6:"entity";b:1;}s:7:"network";a:5:{s:9:"interface";b:1;s:7:"iproute";b:1;s:10:"resolvconf";b:1;s:4:"mail";b:1;s:4:"dhcp";b:1;}s:7:"support";a:1:{s:10:"monitoring";b:1;}s:12:"provisioning";a:2:{s:7:"general";b:1;s:8:"autoprov";b:1;}}}s:7:"service";a:2:{s:4:"ipbx";a:8:{s:11:"queuelogger";a:1:{s:13:"configuration";b:1;}s:16:"general_settings";a:7:{s:4:"sccp";b:1;s:3:"sip";b:1;s:3:"iax";b:1;s:9:"voicemail";b:1;s:9:"phonebook";b:1;s:8:"advanced";b:1;s:11:"outboundmwi";b:1;}s:12:"pbx_settings";a:7:{s:5:"users";b:1;s:5:"lines";b:1;s:7:"devices";b:1;s:6:"groups";b:1;s:6:"meetme";b:1;s:9:"voicemail";b:1;s:9:"extension";b:1;}s:15:"call_management";a:5:{s:6:"incall";b:1;s:7:"outcall";b:1;s:6:"pickup";b:1;s:3:"cel";b:1;s:8:"schedule";b:1;}s:16:"trunk_management";a:3:{s:3:"sip";b:1;s:3:"iax";b:1;s:6:"custom";b:1;}s:12:"pbx_services";a:2:{s:9:"phonebook";b:1;s:13:"extenfeatures";b:1;}s:17:"system_management";a:2:{s:7:"context";b:1;s:10:"extensions";b:1;}s:14:"control_system";a:2:{s:6:"reload";b:1;s:7:"restart";b:1;}}s:10:"callcenter";a:1:{s:8:"settings";a:4:{s:6:"agents";b:1;s:6:"queues";b:1;s:11:"queueskills";b:1;s:15:"queueskillrules";b:1;}}}s:10:"statistics";a:1:{s:11:"call_center";a:2:{s:4:"data";a:4:{s:6:"stats1";b:1;s:6:"stats2";b:1;s:6:"stats3";b:1;s:6:"stats4";b:1;}s:8:"settings";a:1:{s:13:"configuration";b:1;}}}s:3:"cti";a:1:{s:8:"profiles";b:1;}}}',0,'');

COMMIT;

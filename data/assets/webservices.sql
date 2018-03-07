\connect asterisk;

BEGIN;

DELETE FROM "accesswebservice" WHERE NAME = 'xivo-acceptance' AND login = 'xivo-acceptance';
INSERT INTO "accesswebservice" (name, login, passwd, acl) VALUES ('xivo-acceptance', 'xivo-acceptance', 'proformatique', '{auth.#, confd.#, dird.#, agentd.#, ctid-ng.#, call-logd.#}');
DELETE FROM "accesswebservice" WHERE NAME = 'test' AND login = 'admin';
INSERT INTO "accesswebservice" (name, login, passwd, description) VALUES ('test', 'admin', 'proformatique', '');

COMMIT;

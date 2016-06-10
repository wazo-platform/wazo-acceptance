\connect asterisk;

BEGIN;

DELETE FROM "accesswebservice" WHERE NAME = 'xivo-acceptance' AND login = 'xivo-acceptance';
INSERT INTO "accesswebservice" (name, login, passwd, acl) VALUES ('xivo-acceptance', 'xivo-acceptance', 'proformatique', '{confd.#, dird.#, agentd.#, ctid-ng.#}');
DELETE FROM "accesswebservice" WHERE NAME = 'test' AND login = 'admin';
INSERT INTO "accesswebservice" (name, login, passwd, description) VALUES ('test', 'admin', 'proformatique', '');

COMMIT;

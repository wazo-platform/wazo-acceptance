\connect asterisk;

BEGIN;

DELETE FROM "accesswebservice" WHERE NAME = 'test' AND login = 'admin';
INSERT INTO "accesswebservice" (name, login, passwd, description) VALUES ('test', 'admin', 'proformatique', '');

COMMIT;



\connect asterisk;

BEGIN;

DELETE FROM "accesswebservice";
INSERT INTO "accesswebservice" (name, login, passwd, description) VALUES ('test', 'admin', 'proformatique', '');

COMMIT;

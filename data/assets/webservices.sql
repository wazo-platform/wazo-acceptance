\connect asterisk;

BEGIN;

INSERT INTO "accesswebservice" (name, login, passwd, description) VALUES ('test', 'admin', 'proformatique', '');

COMMIT;

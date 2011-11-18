#!/bin/sh

rm -f /etc/pf-xivo/web-interface/xivo.ini
/etc/init.d/postgresql restart
su postgres -c 'psql -c "drop database if exists asterisk;"'
su postgres -c 'psql -c "drop database if exists xivo;"'


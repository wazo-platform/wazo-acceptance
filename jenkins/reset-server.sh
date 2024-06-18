#!/bin/bash

set -xeuo pipefail

if ! dpkg-query -l wazo-platform > /dev/null; then
   echo 'Wazo is not installed'
   exit 1
fi

grep -q 'jenkins@jenkins' .ssh/authorized_keys || echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDF+58PJ/ocRGJDWAsXRreMVmXVpFEIRQCQeNrg0mLq9088HrQl04xSkTtwWdoqdGVbN10x57lMJlEu0QX/ZydHF4itTCFlexa0V47eoarB8ble5aEoyOexxNb1W0QMhSdyF6fXKY8Ws79hUnvkNBPF5KxToPbVy4S1WXvbwEp0g5dkXypUCo+2YTchEcoQf3pB2T+lNMF4lzpkBfCtWj04kaejwTdKZQnolM5ki1D4GjrKoTmGXROzwIpkIxi0zorHrWU2NAObGuHAQNLfAqQqU4zrsgttiisehlCHz8xhogpI/XDo6DSf5WMAobqMp/uDlU7Gge2RQNsPxVyzn/L1 jenkins@jenkins" >> .ssh/authorized_keys

# This key is only used by python/acceptance code, not by jenkins step itself
grep -q 'jenkins@acceptance-ci' .ssh/authorized_keys || echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIGrxKbDH7RkCTZ8dH/iYuf6R5YhBoe6iWOopMO8C3VAv jenkins@acceptance-ci" >> .ssh/authorized_keys


# Remove the UUID from /etc/systemd/system.conf to make xivo-configure-uuid think that the uuid is not configured
# sed -i 's/^DefaultEnvironment=.*/#DefaultEnvironment=/' /etc/systemd/system.conf
# xivo-configure-uuid

# reset the DB, so that we can run the tests twice on the same machine without reinstall

sudo -u postgres psql <<EOF
SELECT pg_terminate_backend(pg_stat_activity.pid)
   FROM pg_stat_activity
   WHERE pg_stat_activity.datname = 'asterisk'
     AND pid <> pg_backend_pid();
EOF

wazo-reset -f
# fail2ban-client set asterisk-wazo addignoreip jenkins.lan.wazo.io

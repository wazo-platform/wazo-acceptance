#!/bin/bash

LOG_DIR=/tmp/commands
mkdir -p ${LOG_DIR}

log(){
    local dest=${LOG_DIR}/$(echo "$*" | sed -e 's/ /_/g').txt
    echo "Running '$* &$> $dest'"
    $* &> $dest
}

log ip addr show
log netstat -laputen
log df
log mount
log systemctl -l show
log systemctl -l
log free -m

for service in $(systemctl list-unit-files | awk '/\<enabled\>/{print $1}'); do
    log journalctl -u $service
done

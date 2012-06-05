#!/bin/bash -x

##########################################
# Following variable must be set manually
# Syntax : 192\\.168\\.1\\.1
#
allowed_host=''
#
# Thank you :)
###########################################

nb_allow_lines=$(grep -e '^allow ' /etc/munin/munin-node.conf -c)

if [[ "$nb_allow_lines" -eq '1' ]]
then
    sed -i -e "/^allow /a allow ^${allowed_host}\$" -e 's/^host 127.0.0.1/host */' /etc/munin/munin-node.conf 
    
fi

exit 0

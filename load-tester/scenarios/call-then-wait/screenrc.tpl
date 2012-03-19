source /etc/screenrc

screen sipp -inf users.csv -sf scenario.xml -s {{ called_exten }} -r {{ sipp_call_rate }} -i {{ sipp_local_ip }} {{ sipp_remote_host }}


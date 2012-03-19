source /etc/screenrc

screen sipp -inf users.csv -sf scenario.xml -d {{ sipp_pause_in_ms }} -s {{ called_exten }} -r {{ sipp_call_rate }} -i {{ sipp_local_ip }} {{ sipp_remote_host }}


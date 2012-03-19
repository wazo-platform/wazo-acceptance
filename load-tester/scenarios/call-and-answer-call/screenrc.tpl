source /etc/screenrc

split
screen sipp -inf users-answer-call.csv -sf scenario-answer-call.xml -i {{ sipp_local_ip }} -p {{ called_line.bind_port }} {{ sipp_remote_host }}
title callee

sleep 1
focus down
resize +4
screen sipp -inf users-call.csv -sf scenario-call.xml -d {{ sipp_pause_in_ms }} -s {{ called_line.exten }} -r {{ sipp_call_rate }} -i {{ sipp_local_ip }} {{ sipp_remote_host }}
title caller


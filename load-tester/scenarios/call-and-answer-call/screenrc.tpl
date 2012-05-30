source /etc/screenrc

split
screen sipp -sf scenario-answer-call.xml -p {{ bind_port }} {{ sipp_std_options }} {{ sipp_remote_host }}
title callee

sleep 1
focus down
resize +4
screen sipp -inf users-call.csv -sf scenario-call.xml -s {{ called_exten }} {{ sipp_std_options }} {{ sipp_remote_host }}
title caller


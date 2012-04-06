source /etc/screenrc

split
screen sipp -inf users-answer-call.csv -sf scenario-answer-call.xml -p {{ called_line.bind_port }} {{ sipp_std_options }} {{ sipp_remote_host }}
title callee

sleep 1
focus down
resize +4
screen sipp -inf users-call.csv -sf scenario-call.xml -s {{ called_exten }} {{ sipp_std_options }} {{ sipp_remote_host }}
title caller


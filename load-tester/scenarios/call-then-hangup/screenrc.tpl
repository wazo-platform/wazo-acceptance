source /etc/screenrc

screen sipp -inf users.csv -sf scenario.xml -s {{ called_exten }} {{ sipp_std_options }} {{ sipp_remote_host }}


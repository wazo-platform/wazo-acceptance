source /etc/screenrc

screen sipp -inf users.csv -sf scenario.xml {{ sipp_std_options }} {{ sipp_remote_host }}


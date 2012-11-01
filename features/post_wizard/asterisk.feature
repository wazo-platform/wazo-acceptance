Feature: Asterisk

    Scenario: Command core reload
        Asterisk command "core reload" return no error

    Scenario: Restart
        When I stop Asterisk
        Then service "asterisk" not run
        Then service "xivo-ctid" not run
        I expected that the service "asterisk" restart
        When service "asterisk" run
        I expected that the service "xivo-ctid" restart
        When service "xivo-ctid" run
        Then I see in the log file service restarted by monit

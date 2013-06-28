Feature: Asterisk

    Scenario: Command core reload
        Asterisk command "core reload" return no error

    Scenario: Restart
        When I stop Asterisk
        When I wait for the service "asterisk" to stop
        Then the service "asterisk" is no longer running
        Then the service "xivo-ctid" is no longer running
        When I wait for the service "asterisk" to restart
        Then the service "asterisk" is running
        When I wait for the service "xivo-ctid" to restart
        Then the service "xivo-ctid" is running
        Then I see in the log file service restarted by monit

    Scenario: Reloading module chan_sccp does not leak a file descriptor
        Given I check the number of file descriptor for asterisk
        When I reload the module chan_sccp.so
        Then I should have the same number of open file descriptor
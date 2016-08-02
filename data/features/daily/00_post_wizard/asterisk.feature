Feature: Asterisk

    Scenario: Asterisk Max File Descriptors
        Then max open file descriptors are equals to 8192

    Scenario: Asterisk Voicemail Directory
        Then directory of the Asterisk voicemail is empty

    Scenario: Sound Files Installed
        Then Asterisk sound files correctly installed

    Scenario: Asterisk Owns Dahdi
        Then Asterisk owns /dev/dadhi

    Scenario: Asterisk MOH files Permission
        Then MOH files owned by asterisk:www-data

    Scenario: Command core reload
        Asterisk command "core reload" return no error

    Scenario: Restart
        When I stop "asterisk"
        When I wait for the service "asterisk" to stop
        Then the service "asterisk" is no longer running
        Then the service "xivo-ctid" is no longer running
        When I wait for the service "asterisk" to restart
        Then the service "asterisk" is running
        When I wait for the service "xivo-ctid" to restart
        Then the service "xivo-ctid" is running
        Then I see in the log file service restarted by monit

    Scenario: Monit password
        Given I change the "xivo_monit_user" AMI password to "secret"
        Then asterisk should be restarted in the following "5" minutes

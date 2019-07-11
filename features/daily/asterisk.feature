Feature: Asterisk

    Scenario: Asterisk is correctly installed
        Then Asterisk may open at most 8192 file descriptors
        Then Asterisk sound files are correctly installed
        Then Asterisk owns /dev/dadhi
        Then MOH files are owned by asterisk:www-data
        Then Asterisk command "core reload" returns no error

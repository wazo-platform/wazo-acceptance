Feature: Asterisk

  Scenario: Asterisk is correctly installed
    Then Asterisk may open at most "8192" file descriptors
    Then Asterisk sound files are correctly installed
    Then MOH files are owned by asterisk:www-data
    Then the service "asterisk" is running
    Then the service "asterisk" has priority "-11"

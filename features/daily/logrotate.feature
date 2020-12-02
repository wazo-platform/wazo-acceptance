Feature: Logrotate

  Scenario: Call logs are still working after a log rotate
    When I execute the logrotate command for service "asterisk"
    Then the file "/var/log/asterisk/full" is not empty

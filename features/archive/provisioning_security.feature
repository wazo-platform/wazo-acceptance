Feature: Provisioning security

    Scenario: Fail2ban test for xivo-provd
        Given there's no plugins "xivo-aastra" installed
        Given the latest plugin "xivo-aastra" is installed
        Given there are no devices with mac "00:11:22:33:44:55"
        Given the file "/var/log/xivo-provd-fail2ban.log" is empty
        When the provisioning server receives the following HTTP requests:
          | path                    | user-agent                                        |
          | Aastra/001122334455.cfg | Aastra6863i MAC:00-11-22-33-44-55 V:4.1.0.128-SIP |
        Then fail2ban-regex for "xivo-provd" matches 2 lines

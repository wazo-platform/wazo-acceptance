Feature: Provisioning security

  Scenario: Fail2ban test for wazo-provd
    Given the latest plugin "xivo-aastra" is installed
    Given the file "/var/log/wazo-provd-fail2ban.log" is empty
    When the following devices are created via HTTP requests to the provisioning server:
      | mac               | path                    | user-agent                                        |
      | 00:11:22:33:44:55 | Aastra/001122334455.cfg | Aastra6863i MAC:00-11-22-33-44-55 V:4.1.0.128-SIP |
    Then fail2ban-regex for "wazo-provd" matches 2 lines

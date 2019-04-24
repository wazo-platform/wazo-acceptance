Feature: Synchronize

    Scenario: Synchronize two devices behind NAT
        Given the latest plugin "xivo-aastra" is installed
        Given I have the following devices:
          | mac               | latest plugin of |
          | 00:11:22:33:44:01 | xivo-aastra      |
          | 00:11:22:33:44:02 | xivo-aastra      |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |            device |
          | User      | 01       |   1001 | default | sip      | 00:11:22:33:44:01 |
          | User      | 02       |   1002 | default | sip      | 00:11:22:33:44:02 |
        Given the provisioning server has received the following HTTP requests:
          | path                    | user-agent                                         |
          | Aastra/001122334401.cfg | Aastra6731i MAC:00-11-22-33-44-01 V:3.2.2.1136-SIP |
          | Aastra/001122334402.cfg | Aastra6731i MAC:00-11-22-33-44-02 V:3.2.2.1136-SIP |
        Given the AMI is monitored
        When I synchronize the device with mac "00:11:22:33:44:01"
        Then I see in the AMI that the line "1001@default" has been synchronized
        When I synchronize the device with mac "00:11:22:33:44:02"
        Then I see in the AMI that the line "1002@default" has been synchronized

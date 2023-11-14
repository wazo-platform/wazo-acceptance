Feature: Provisioning

  Scenario: Fail2ban test for wazo-provd
    Given the plugin "wazo-yealink" version "v86" is installed
    Given the file "/var/log/wazo-provd-fail2ban.log" is empty
    When the following devices are created via HTTP requests to the provisioning server:
      | mac               | path             | user-agent                                       |
      | 80:5e:c0:d5:7d:55 | 805ec0d57d55.cfg | Yealink SIP-T31G 124.85.257.55 80:5e:c0:d5:7d:55 |
    Then fail2ban-regex for "wazo-provd" matches 2 lines

  Scenario: Synchronize two devices behind NAT
    Given the plugin "wazo-aastra" version "5.0.0" is installed
    Given the plugin "wazo-polycom" version "5.8.2" is installed
    Given there are devices with infos:
      | mac               | plugin version         |
      | 00:11:22:33:44:01 | wazo-aastra-5.0.0      |
      | 00:11:22:33:44:02 | wazo-polycom-5.8.2     |
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | protocol | device            |
      | User      | 01       | 1001  | default | sip      | 00:11:22:33:44:01 |
      | User      | 02       | 1002  | default | sip      | 00:11:22:33:44:02 |
    Given the following devices are created via HTTP requests to the provisioning server:
      | path                    | user-agent                                                      |
      | Aastra/001122334401.cfg | Aastra6873i MAC:00-11-22-33-44-01 V:5.0.0.1018-SIP              |
      | 001122334402-user.cfg   | FileTransport PolycomVVX-VVX_101-UA/5.4.3.1014 Type/Application |
    When I synchronize the device with mac "00:11:22:33:44:01"
    Then I see in the AMI that the line "1001@default" has been synchronized
    When I synchronize the device with mac "00:11:22:33:44:02"
    Then I see in the AMI that the line "1002@default" has been synchronized

  Scenario: HTTPS provisioning
    Given the plugin "wazo-polycom" version "5.8.2" is installed
    Given there are devices with infos:
      | mac               | plugin version         |
      | 00:11:22:33:44:55 | wazo-polycom-5.8.2     |
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | protocol | device            |
      | User      | 02       | 1002  | default | sip      | 00:11:22:33:44:55 |
    Then the following provisioning files are available over HTTPS:
      | path                  | user-agent                                                      | expected_content |
      | 001122334455-user.cfg | FileTransport PolycomVVX-VVX_101-UA/5.4.3.1014 Type/Application | <polycomConfig   |

  Scenario: URL Key provisioning
    Given the provd HTTP auth strategy is set to "url_key"
    Given the provisioning key is "secure123"
    Given the plugin "wazo-polycom" version "5.8.2" is installed
    Given there are devices with infos:
      | mac               | plugin version         |
      | 00:11:22:33:44:99 | wazo-polycom-5.8.2     |
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | protocol | device            |
      | User      | 02       | 1002  | default | sip      | 00:11:22:33:44:99 |
    Then the following provisioning files are available over HTTPS using provisioning key "secure123":
      | path                  | user-agent                                                      | expected_content |
      | 001122334499-user.cfg | FileTransport PolycomVVX-VVX_101-UA/5.4.3.1014 Type/Application | <polycomConfig   |

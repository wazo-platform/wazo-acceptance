Feature: Devices

    Scenario: Search
        Given I have the following devices:
          | ip             | mac               |
          | 192.168.32.197 | 00:00:00:00:aa:01 |
          | 192.168.32.198 | 00:00:00:00:bb:02 |
        When I search device "bb:02"
        Then the search results are:
          | present           | not present       |
          | 00:00:00:00:bb:02 | 00:00:00:00:aa:01 |
        When I search device "197"
        Then the search results are:
          | present           | not present       |
          | 00:00:00:00:aa:01 | 00:00:00:00:bb:02 |

    Scenario: Search devices by number
        Given I have the following users:
            | firstname | lastname |
            | Richard   | Stallman |
        Given I have the following lines:
            | context | protocol | username       | secret         | device_slot |
            | default | sip      | devicebynumber | devicebynumber | 1           |
        Given I have the following extensions:
            | context | exten |
            | default |  1000 |
        Given I have the following devices:
          | ip             | mac               |
          | 192.168.32.104 | 00:00:00:00:aa:02 |
          | 192.168.32.10  | 00:00:00:00:cc:22 |
        Given SIP line "devicebynumber" is associated to extension "1000@default"
        Given SIP line "devicebynumber" is associated to user "Richard" "Stallman"
        When I provision device having ip "192.168.32.104" with line having username "devicebynumber"
        When I search device by number "1000"
        Then the search results are:
          | present           | not present       |
          | 00:00:00:00:aa:02 | 00:00:00:00:cc:22 |

    Scenario: List
        When I request devices in the webi
        Then the confd REST API received a request with infos:
          | method | path         |
          | GET    | /1.1/devices |

    Scenario: Create
        When I create the device with infos:
          |            ip | mac               |
          | 192.168.32.21 | 00:00:00:00:bb:02 |
        Then the confd REST API received a request with infos:
          | method | path         |
          | POST   | /1.1/devices |

    Scenario: Edit
        Given I have the following devices:
          |             ip | mac               |
          | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I edit the device with mac "00:00:00:00:aa:01" via webi with infos:
          | description    |
          | toto           |
        Then the confd REST API received a request with infos:
          | method | path             | data                                                                                                                                       |
          | PUT    | /1.1/devices/\w+  | {"ip":"192.168.32.197","mac":"00:00:00:00:aa:01","template_id":"defaultconfigdevice","description":"toto","options":{"switchboard":false}} |

    Scenario: Edit the switchboard option
        Given the plugin "null" is installed
        Given there's no plugins "xivo-aastra" installed
        Given the latest plugin "xivo-aastra" for "67XXi" is installed
        Given I have the following devices:
          |             ip | mac               | vendor | model | plugin |
          | 192.168.32.197 | 00:00:00:00:aa:01 | Aastra | 6757i | null   |
        When I open the edit page of the device with mac "00:00:00:00:aa:01"
        Then the web interfaces shows a device with:
          | switchboard_enabled | switchboard_checked |
          | False               | False               |
        When I select a plugin "xivo-aastra-3.3.1-SP4"
        Then the web interfaces shows a device with:
          | switchboard_enabled | switchboard_checked |
          | True                | False               |
        When I check the switchboard checkbox
        When I submit the form
        When I open the edit page of the device with mac "00:00:00:00:aa:01"
        Then the web interfaces shows a device with:
          | switchboard_enabled | switchboard_checked |
          | True                | True                |

    Scenario: Delete
        Given I have the following devices:
          |             ip | mac               |
          | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I delete the device with mac "00:00:00:00:aa:01" via webi
        Then the confd REST API received a request with infos:
          | method | path                         |
          | DELETE | /1.1/devices/\w+ |
        Then there is no device "00:00:00:00:aa:01"

    Scenario: Delete a device associated to a line
        Given I have the following devices:
          |       ip | mac               |
          | 10.0.0.1 | 00:00:00:fa:1c:01 |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |            device |
          | Han       | Solo     |   1138 | default | sip      | 00:00:00:fa:1c:01 |
        When I delete the device with mac "00:00:00:fa:1c:01" via webi
        Then there is no device "00:00:00:fa:1c:01"

    Scenario: Update device slot
        Given I have the following devices:
          | mac               |
          | 00:00:00:11:22:33 |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |            device |
          | Han       | Solo     |   1138 | default | sip      | 00:00:00:11:22:33 |
         When I modify the device slot of user "Han" "Solo" to "2"
         When I modify the device slot of user "Han" "Solo" to "1"
         Then I see no errors

    Scenario: Associate and dissociate multiple lines to device
        Given I have the following devices:
          | mac               |
          | 00:00:00:11:22:33 |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |            device | device_slot |
          | Han       | Solo     |   1138 | default | sip      | 00:00:00:11:22:33 | 1           |
          | Han       | Duo      |   1139 | default | sip      | 00:00:00:11:22:33 | 2           |
        When I modify the device of user "Han" "Duo" to ""
        When I modify the device of user "Han" "Duo" to "00:00:11:22:33" with device slot "2"
        When I modify the device of user "Han" "Solo" to ""
        When I modify the device of user "Han" "Duo" to ""
        Then I see no errors

    Scenario: Autoprov
        Given I have the following devices:
          |             ip | mac               |
          | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I reset to autoprov the device with mac "00:00:00:00:aa:01" from webi
        Then the confd REST API received a request with infos:
          | method | path                                    |
          | GET    | /1.1/devices/\w+/autoprov    |
          | GET    | /1.1/devices/\w+/synchronize |

    Scenario: Provision
        Given I have the following users:
            | firstname     | lastname |
            | Provisionable | NiceGuy  |
        Given I have the following lines:
            | context | protocol | username        | secret          | device_slot |
            | default | sip      | deviceprovision | deviceprovision | 1           |
        Given I have the following extensions:
            | context | exten |
            | default |  1000 |
        Given I have the following devices:
          | ip             | mac               |
          | 192.168.32.104 | 00:00:00:00:aa:02 |
          | 192.168.32.10  | 00:00:00:00:cc:22 |
          | 192.168.32.101 | 00:00:00:00:aa:05 |
          | 192.168.32.1   | 00:00:00:00:bb:09 |
        Given SIP line "deviceprovision" is associated to extension "1000@default"
        Given SIP line "deviceprovision" is associated to user "Provisionable" "NiceGuy"
        When I provision device having ip "192.168.32.1" with line having username "deviceprovision"
        Then the device with mac "00:00:00:00:bb:09" has been provisioned with a configuration:
            | display_name          | number | username        | auth_username   | password        |
            | Provisionable NiceGuy | 1000   | deviceprovision | deviceprovision | deviceprovision |

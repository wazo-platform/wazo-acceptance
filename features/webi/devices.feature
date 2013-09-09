Feature: Devices

    Scenario: Search
        Given I have the following devices:
          | ip             | mac               |
          | 192.168.32.197 | 00:00:00:00:aa:01 |
          | 192.168.32.198 | 00:00:00:00:bb:02 |
        When I search device "bb:02"
        Then device "00:00:00:00:bb:02" is displayed in the list
        Then device "00:00:00:00:aa:01" is not displayed in the list
        When I search device "197"
        Then device "00:00:00:00:aa:01" is displayed in the list
        Then device "00:00:00:00:bb:02" is not displayed in the list

    Scenario: List
        When I request devices in the webi
        Then the REST API received a request with infos:
          | method | path         |
          | GET    | /1.1/devices |

    Scenario: Create
        Given there are no devices with mac "00:00:00:00:bb:02"
        When I create the device with infos:
          | ip             | mac               |
          | 192.168.54.219 | 00:00:00:00:bb:02 |
        Then the REST API received a request with infos:
          | method | path         |
          | POST   | /1.1/devices |

    Scenario: Edit
        Given there are no devices with id "123"
        Given I have the following devices:
          | id  | ip             | mac               |
          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I edit the device "123" with infos:
          | ip             |
          | 192.168.54.219 |
        Then the REST API received a request with infos:
          | method | path         | data                     |
          | PUT    | /1.1/devices/ | {"ip": "192.168.54.219"} |

    Scenario: Delete
        Given there are no devices with id "123"
        Given I have the following devices:
          | id  | ip             | mac               |
          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I delete the device "123"
        Then the REST API received a request with infos:
          | method | path         | data                     |
          | DELETE | /1.1/devices | {"ip": "192.168.54.219"} |

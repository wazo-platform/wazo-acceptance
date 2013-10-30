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

    Scenario: List
        When I request devices in the webi
        Then the REST API received a request with infos:
          | method | path         |
          | GET    | /1.1/devices |

    Scenario: Create
        Given there are no devices with mac "00:00:00:00:bb:02"
        When I create the device with infos:
          | ip             | mac               |
          | 192.168.32.21 | 00:00:00:00:bb:02 |
        Then the REST API received a request with infos:
          | method | path         |
          | POST   | /1.1/devices |

    Scenario: Edit
        Given there are no devices with id "123"
        Given I have the following devices:
          | id  | ip             | mac               |
          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I edit the device "123" with infos:
          | description    |
          | toto           |
        Then the REST API received a request with infos:
          | method | path             | data                                                                                                       |
          | PUT    | /1.1/devices/123 | {"ip":"192.168.32.197","mac":"00:00:00:00:aa:01","template_id":"defaultconfigdevice","description":"toto"} |

    Scenario: Delete
        Given there are no devices with id "123"
        Given I have the following devices:
          | id  | ip             | mac               |
          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I delete the device "123"
        Then the REST API received a request with infos:
          | method | path             |
          | DELETE | /1.1/devices/123 |

#    Scenario: Synchronize
#       Given there are no devices with id "123"
#        Given I have the following devices:
#          | id  | ip             | mac               |
#          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
#        When I synchronize the device with mac "00:00:00:00:aa:01" from webi
#        Then the REST API received a request with infos:
#          | method | path                 |
#          | GET    | /1.1/devices/123/synchronize |

    Scenario: Autoprov
        Given there are no devices with id "123"
        Given I have the following devices:
          | id  | ip             | mac               |
          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I reset to autoprov the device with mac "00:00:00:00:aa:01" from webi
        Then the REST API received a request with infos:
          | method | path                 |
          | GET    | /1.1/devices/123/autoprov    |
          | GET    | /1.1/devices/123/synchronize |

    Scenario: Provision
        Given there are no devices with id "222"
        Given there are no devices with id "333"
        Given there are no devices with id "444"
        Given there are no devices with id "888"
        Given I only have the following users:
            | id | firstname | lastname  |
            | 1  | Greg      | Sanderson |
        Given I only have the following lines:
            | id | context | protocol | username | secret | device_slot |
            | 10 | default | sip      | toto     | tata   | 1           |
        Given I only have the following extensions:
            | id  | context | exten |
            | 100 | default | 1000  |
        Given I have the following devices:
          | id  | ip             | mac               |
          | 222 | 192.168.32.104 | 00:00:00:00:aa:02 |
          | 333 | 192.168.32.10  | 00:00:00:00:cc:22 |
          | 444 | 192.168.32.101 | 00:00:00:00:aa:05 |
          | 888 | 192.168.32.1   | 00:00:00:00:bb:09 |
        When I create the following links:
            | user_id | line_id | extension_id |
            | 1       | 10      | 100          |
        Then I get a response with status "201"
        When I provision my device with my line_id "10" and ip "192.168.32.1"
        Then the device "888" has been provisioned with a configuration:
            | display_name   | number | username | auth_username | password |
            | Greg Sanderson | 1000   | toto     | toto          | tata     |

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
          |            ip | mac               |
          | 192.168.32.21 | 00:00:00:00:bb:02 |
        Then the REST API received a request with infos:
          | method | path         |
          | POST   | /1.1/devices |

    Scenario: Edit
        Given there are no devices with id "564635464951957"
        Given I have the following devices:
          |              id |             ip | mac               |
          | 564635464951957 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I edit the device "564635464951957" with infos:
          | description    |
          | toto           |
        Then the REST API received a request with infos:
          | method | path                         | data                                                                                                       |
          | PUT    | /1.1/devices/564635464951957 | {"ip":"192.168.32.197","mac":"00:00:00:00:aa:01","template_id":"defaultconfigdevice","description":"toto"} |

    Scenario: Delete
        Given there are no devices with id "542135468456498"
        Given I have the following devices:
          |              id |             ip | mac               |
          | 542135468456498 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I delete the device "542135468456498"
        Then the REST API received a request with infos:
          | method | path                         |
          | DELETE | /1.1/devices/542135468456498 |
        Then there is no device "00:00:00:00:aa:01"

    Scenario: Delete a device associated to a line
        Given I have the following devices:
          |               id |       ip | mac               |
          | 1654324689546246 | 10.0.0.1 | 00:00:00:fa:1c:01 |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |            device |
          | Han       | Solo     |   1138 | default | sip      | 00:00:00:fa:1c:01 |
        When I delete the device "1654324689546246"
        Then there is no device "00:00:00:fa:1c:01"

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
        Given there are no devices with id "62144354987621"
        Given I have the following devices:
          |             id |             ip | mac               |
          | 62144354987621 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I reset to autoprov the device with mac "00:00:00:00:aa:01" from webi
        Then the REST API received a request with infos:
          | method | path                                    |
          | GET    | /1.1/devices/62144354987621/autoprov    |
          | GET    | /1.1/devices/62144354987621/synchronize |

    Scenario: Provision
        Given there are no devices with id "9845946546546"
        Given there are no devices with id "6241621649541"
        Given there are no devices with id "9546216549495"
        Given there are no devices with id "1495162494654"
        Given I have the following users:
            |     id | firstname | lastname  |
            | 984346 | Greg      | Sanderson |
        Given I have the following lines:
            |     id | context | protocol | username | secret | device_slot |
            | 654134 | default | sip      | toto     | tata   |           1 |
        Given I have the following extensions:
            |     id | context | exten |
            | 135477 | default |  1000 |
        Given I have the following devices:
          |            id |             ip | mac               |
          | 9845946546546 | 192.168.32.104 | 00:00:00:00:aa:02 |
          | 6241621649541 |  192.168.32.10 | 00:00:00:00:cc:22 |
          | 9546216549495 | 192.168.32.101 | 00:00:00:00:aa:05 |
          | 1495162494654 |   192.168.32.1 | 00:00:00:00:bb:09 |
        Given line "654134" is linked with extension "1000@default"
        Given line "654134" is linked with user id "984346"
        When I provision my device with my line_id "654134" and ip "192.168.32.1"
        Then the device "1495162494654" has been provisioned with a configuration:
            | display_name   | number | username | auth_username | password |
            | Greg Sanderson | 1000   | toto     | toto          | tata     |

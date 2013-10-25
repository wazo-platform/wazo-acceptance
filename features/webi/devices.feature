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
        Then there is no device "00:00:00:00:aa:01"

    Scenario: Delete a device associated to a line
        Given I have the following devices:
          | id |       ip | mac               |
          | 20 | 10.0.0.1 | 00:00:00:fa:1c:01 |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |            device |
          | Han       | Solo     |   1138 | default | sip      | 00:00:00:fa:1c:01 |
        When I delete the device "20"
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
        Given there are no devices with id "123"
        Given I have the following devices:
          | id  | ip             | mac               |
          | 123 | 192.168.32.197 | 00:00:00:00:aa:01 |
        When I reset to autoprov the device with mac "00:00:00:00:aa:01" from webi
        Then the REST API received a request with infos:
          | method | path                 |
          | GET    | /1.1/devices/123/autoprov    |
          | GET    | /1.1/devices/123/synchronize |

Feature: SCCP Line

    Scenario: Customize codecs
        Given there are users with infos:
          | firstname | lastname | number | context | protocol |
          | Robert    |          |   1762 | default | sccp     |
        When I customize line "1762" codecs to:
          | codec               |
          | G.711 A-law (Audio) |
          | G.729A (Audio)      |
        Then the "1762" section of "sccp.conf" contains the options:
          | name     | value      |
          | disallow | all        |
          | allow    | alaw,g729  |
        When I disable line codecs customization for line "1762"
        Then the "1762" section of "sccp.conf" does not contain the options:
          | name     |
          | disallow |
          | allow    |

    Scenario: Delete SCCP line from user resetting device to autoprov
        Given the latest plugin "xivo-cisco-sccp-legacy" is installed
        Given I have the following devices:
          | mac               | latest plugin of       |
          | 11:11:11:11:11:11 | xivo-cisco-sccp-legacy |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol | device            | entity_name |
          | Albert    |  qwerty  | 1111   | default | sccp     | 11:11:11:11:11:11 | xivo_entity |
        When I remove line from user "Albert" "qwerty"
        When I go get the device with mac "11:11:11:11:11:11" using its id
        Then the device has the following parameters:
          | status   |
          | autoprov |

    Scenario: Delete user with SCCP line resetting device to autoprov
        Given the latest plugin "xivo-cisco-sccp-legacy" is installed
        Given I have the following devices:
          | mac               | latest plugin of       |
          | 11:11:11:11:11:12 | xivo-cisco-sccp-legacy |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol | device            | entity_name |
          | Albert    |  qwerty  | 1112   | default | sccp     | 11:11:11:11:11:12 | xivo_entity |
        When I remove user "Albert" "qwerty"
        When I go get the device with mac "11:11:11:11:11:12" using its id
        Then the device has the following parameters:
          | status   |
          | autoprov |

    Scenario: Remove device from user resetting device to autoprov
        Given the latest plugin "xivo-cisco-sccp-legacy" is installed
        Given I have the following devices:
          | mac               | latest plugin of       |
          | 11:11:11:11:11:13 | xivo-cisco-sccp-legacy |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol | device            | entity_name |
          | Albert    |  qwerty  |   1113 | default | sccp     | 11:11:11:11:11:13 | xivo_entity |
        When I modify the device of user "Albert" "qwerty" to ""
        When I go get the device with mac "11:11:11:11:11:13" using its id
        Then the device has the following parameters:
          | status   |
          | autoprov |

    Scenario: Change device of user resetting old device to autoprov
        Given the latest plugin "xivo-cisco-sccp-legacy" is installed
        Given I have the following devices:
          | mac               | latest plugin of       |
          | 11:11:11:11:11:14 | xivo-cisco-sccp-legacy |
          | 11:11:11:11:11:15 | xivo-cisco-sccp-legacy |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol | device            | entity_name |
          | Albert    |  qwerty  |   1113 | default | sccp     | 11:11:11:11:11:14 | xivo_entity |
        When I modify the device of user "Albert" "qwerty" to "11:11:11:11:11:15"
        When I go get the device with mac "11:11:11:11:11:14" using its id
        Then I get a response with a link to the "devices" resource
        Then the device has the following parameters:
          | status   |
          | autoprov |
        When I go get the device with mac "11:11:11:11:11:15" using its id
        Then the device has the following parameters:
          | status     |
          | configured |

#    Scenario: Replace SCCP line with SIP line resetting SCCP device to autoprov
#        Given the latest plugin "xivo-cisco-sccp-legacy" is installed
#        Given I have the following devices:
#          | mac               | latest plugin of       |
#          | 11:11:11:11:11:16 | xivo-cisco-sccp-legacy |
#          | 11:11:11:11:11:17 | xivo-aastra            |
#        Given there are users with infos:
#          | firstname | lastname | number | context | protocol | device            | entity_name |
#          | Albert    |  qwerty  |   1113 | default | sccp     | 11:11:11:11:11:16 | xivo_entity |
#        When I add a new line to user "Albert" "qwerty" with infos:
#          | number | context | protocol | device            | entity_displayname |
#          | 1113   | default | SIP      | 11:11:11:11:11:17 | xivo_entity        |
#        When I go get the device with mac "11:11:11:11:11:16" using its id
#        Then the device has the following parameters:
#          | status   |
#          | autoprov |
#        When I go get the device with mac "11:11:11:11:11:17" using its id
#        Then the device has the following parameters:
#          | status     |
#          | configured |

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
          | Albert    |  qwerty  | 1111   | default | sccp     | 11:11:11:11:11:11 | xivoentity  |
        When I remove line from user "Albert" "qwerty"
        Then I see devices with infos:
          |               mac | configured |
          | 11:11:11:11:11:11 | False      |

    Scenario: Delete user with SCCP line resetting device to autoprov
        Given the latest plugin "xivo-cisco-sccp-legacy" is installed
        Given I have the following devices:
          | mac               | latest plugin of       |
          | 11:11:11:11:11:12 | xivo-cisco-sccp-legacy |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol | device            | entity_name |
          | Albert    |  qwerty  | 1112   | default | sccp     | 11:11:11:11:11:12 | xivoentity  |
        When I remove user "Albert" "qwerty"
        Then I see devices with infos:
          |               mac | configured |
          | 11:11:11:11:11:12 | False      |

    Scenario: Remove device from user resetting device to autoprov
        Given the latest plugin "xivo-cisco-sccp-legacy" is installed
        Given I have the following devices:
          | mac               | latest plugin of       |
          | 11:11:11:11:11:13 | xivo-cisco-sccp-legacy |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol | device            | entity_name |
          | Albert    |  qwerty  |   1113 | default | sccp     | 11:11:11:11:11:13 | xivoentity  |
        When I modify the device of user "Albert" "qwerty" to ""
        Then I see devices with infos:
          |               mac | configured |
          | 11:11:11:11:11:13 | False      |

    Scenario: Change device of user resetting old device to autoprov
        Given the latest plugin "xivo-cisco-sccp-legacy" is installed
        Given I have the following devices:
          | mac               | latest plugin of       |
          | 11:11:11:11:11:14 | xivo-cisco-sccp-legacy |
          | 11:11:11:11:11:15 | xivo-cisco-sccp-legacy |
        Given there are users with infos:
          | firstname | lastname | number | context | protocol | device            | entity_name |
          | Albert    |  qwerty  |   1113 | default | sccp     | 11:11:11:11:11:14 | xivoentity  |
        When I modify the device of user "Albert" "qwerty" to "11:11:11:11:11:15"
        Then I see devices with infos:
          |               mac | configured |
          | 11:11:11:11:11:14 | False      |
          | 11:11:11:11:11:15 | True       |

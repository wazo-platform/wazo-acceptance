Feature: Directed pickup

    Scenario: Pickup a call
        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | User      | 100      |   1100 | default | sip      |
         | User      | 101      |   1101 | default | sip      |
         | User      | 102      |   1102 | default | sip      |

        When "User 100" calls "1101"
        Then "User 101" is ringing
        When "User 102" calls "*81101"
        Then "User 100" is talking
        Then "User 102" is talking

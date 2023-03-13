Feature: User API - user managed with one HTTP call

  Scenario: Call to inexistant extension - user created with one HTTP call
    When there are users "wazo_acceptance/assets/1_user.json"
    When "Rîchard Lâpoin" calls "1190"
    Then "Rîchard Lâpoin" is hungup immediately

  Scenario: Call to existant extension with answer - user created with one HTTP call
    When there are users "wazo_acceptance/assets/2_users.json"
    When a call is started:
      | caller          | dial | callee      | talk_time | hangup | ring_time |
      | Rîchard Lâpoin  | 1101 | Celine Dion | 3         | callee | 5         |
    Then I have the last call log matching:
      | destination_extension | duration | answered |
      | 1101                  | 3        | True     |

  Scenario: Incall to destination user
    When there are users "wazo_acceptance/assets/1_user.json"
    When chan_test calls "4100@from-extern"
    Then "Rîchard Lâpoin" is ringing

  Scenario: Incall to users group
    Given there are telephony groups with infos:
      | label       | exten | context | timeout | noanswer_destination |
      | test        |  2999 | default |         |                      |
    Given ring group is "test"
    When there are users "wazo_acceptance/assets/3_users.json"
    When chan_test calls "2999@default"
    Then "Rîchard Lâpoin" is ringing
    Then "Celine Dion" is ringing
    Then "James Bond" is ringing

  Scenario: Switchboard
    Given switchboard is "Inn"
    When there are users "wazo_acceptance/assets/1_user.json"
    Given there is an incall "1000@from-extern" to the switchboard "Inn"
    Given I listen on the bus for "switchboard_queued_calls_updated" messages
    When incoming call received from "incall" to "1000@from-extern"
    Then I receive a "switchboard_queued_calls_updated" event
    Then switchboard "Inn" has "incall" in queued calls
    When "Rîchard Lâpoin" answer queued call "incall" from switchboard "Inn"
    Then "Rîchard Lâpoin" is talking to "incall"

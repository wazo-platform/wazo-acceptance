Feature: Groups

  Scenario: Group ring timeout is reset when no timeout
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Andrew    | Wiggin   |  1684 | default |
      | Valentine | Wiggin   |  1438 | default |
    Given there are telephony groups with infos:
      | label       | exten | context | timeout | noanswer_destination |
      | lusitania   |  2514 | default |         |                      |
      | descoladors |  2966 | default | 5       | group:lusitania      |
    Given the telephony group "lusitania" has users:
      | firstname | lastname |
      | Andrew    | Wiggin   |
    When "Valentine Wiggin" calls "2966"
    When I wait 6 seconds for the call to be forwarded
    Then "Andrew Wiggin" is ringing
    When I wait 6 seconds for the timeout to not expire
    Then "Andrew Wiggin" is ringing

  Scenario: Dynamic group member
    Given there are devices with infos:
      | mac               |
      | 00:11:22:33:44:00 |
    Given there are telephony users with infos:
      | firstname | lastname | exten | context | device            | with_phone |
      | Flash     | McQueen  | 1801  | default | 00:11:22:33:44:00 | yes        |
      | Tow       | Mater    | 1802  | default |                   | yes        |
    Given there are telephony groups with infos:
      | label       | exten | context |
      | Dynamic     | 2801  | default |
    Given "Flash McQueen" has function keys:
      | position | destination_type | destination_group_label | destination_action |
      | 1        | groupmember      | Dynamic                 | toggle             |
    When "Flash McQueen" press function key "1"
    When I wait 4 seconds for the call processing
    When "Tow Mater" calls "2801"
    When I wait 2 seconds for the call processing
    Then "Flash McQueen" is ringing
    Then "Tow Mater" hangs up
    When I wait 1 seconds for the call hangs up for everyone
    When "Flash McQueen" press function key "1"
    When I wait 4 seconds for the call processing
    When "Tow Mater" calls "2801"
    When I wait 2 seconds for the call processing
    Then "Flash McQueen" is hungup

Scenario: Group member does not ring when in DND
    Given there are telephony users with infos:
      | firstname  | lastname | exten | context |
      | Leticia    | Gendron  | 1949  | default |
      | Bernandine | Gignac   | 1950  | default |
      | Arnie      | Douglas  | 1951  | default |
    Given there are telephony groups with infos:
      | label       | exten | context |
      | pretonians  | 2515  | default |
    Given the telephony group "pretonians" has users:
      | firstname  | lastname  |
      | Leticia    | Gendron   |
      | Bernandine | Gignac    |
    When "Leticia Gendron" enable DND
    When I wait 2 seconds
    When "Arnie Douglas" calls "2515"
    When I wait 2 seconds for the call processing
    Then "Leticia Gendron" is hungup
    Then "Bernandine Gignac" is ringing

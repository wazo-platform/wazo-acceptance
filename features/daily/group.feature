Feature: Groups

  Scenario: Group ring timeout is reset when no timeout
    Given there are telephony users with infos:
      | firstname | lastname | exten | context |
      | Andrew    | Wiggin   |  1684 | default |
      | Valentine | Wiggin   |  1438 | default |
    Given there are telephony groups with infos:
      | name        | exten | context | timeout | noanswer_destination |
      | lusitania   |  2514 | default |         |                      |
      | descoladors |  2966 | default | 5       | group:lusitania      |
    Given the telephony group "lusitania" has users:
      | firstname | lastname |
      | Andrew    | Wiggin   |
    When "Valentine Wiggin" calls "2966"
    When I wait "6" seconds for the call to be forwarded
    Then "Andrew Wiggin" is ringing
    When I wait "6" seconds for the timeout to not expire
    Then "Andrew Wiggin" is ringing

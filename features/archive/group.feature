Feature: Groups

    Scenario: Group ring timeout is reset when no timeout

        Given there are users with infos:
         | firstname | lastname | number | context | protocol |
         | Andrew    | Wiggin   |   1684 | default | sip      |
         | Valentine | Wiggin   |   1438 | default | sip      |
        Given there is a group "lusitania" with extension "2514@default" and users:
         | firstname | lastname |
         | Andrew    | Wiggin   |
        Given there are groups:
         | name        | exten | context | noanswer        | ring seconds |
         | descoladors |  2966 | default | group:lusitania |            5 |
        When "Valentine Wiggin" calls "2966"
        When I wait 6 seconds for the call to be forwarded
        Then "Andrew Wiggin" is ringing
        When I wait 6 seconds for the timeout to not expire
        Then "Andrew Wiggin" is ringing

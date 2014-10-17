Feature: Switchboard

    Scenario: Answer second incoming call
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | number | context | protocol | agent_number |
         | Switch    | Board    | Switchboard | switch    | board      |   1631 | default | sip      |         1631 |
         | Alice     | A        |             |           |            |   1632 | default | sip      |              |
         | Bob       | B        |             |           |            |   1633 | default | sip      |              |
         | Charlie   | C        |             |           |            |   1634 | default | sip      |              |
        Given there is a switchboard configured as:
         | incalls queue name | hold calls queue name   | incalls queue number | incalls queue context | hold calls queue number | hold calls queue context | agents       |
         | __switchboard-test | __switchboard_hold-test |                 3009 | default               |                    3010 | default                  | 1631@default |
        When I start the XiVO Client
        When I set the switchboard queues:
         | incalls            | on hold                 |
         | __switchboard-test | __switchboard_hold-test |
        When I log in the XiVO Client as "switch", pass "board", logged agent
        When "Alice A" calls "3009"
        When "Bob B" calls "3009"
        When "Charlie C" calls "3009"
        When I wait 3 seconds for the call processing
        When the switchboard "Switch Board" selects the incoming call from "Bob B" number "1633"
        When "Switch Board" answers
        Then the switchboard is talking to "Bob B" number "1633"
        When the switchboard "Switch Board" selects the incoming call from "Charlie C" number "1634"
        Then the switchboard is talking to "Bob B" number "1633"

    Scenario: Hangup received call
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | number | context | protocol | agent_number |
         | Switch    | Board    | Switchboard | switch    | board      |   1438 | default | sip      |         1438 |
         | Alice     | A        |             |           |            |   1439 | default | sip      |              |
        Given there is a switchboard configured as:
         | incalls queue name | hold calls queue name   | incalls queue number | incalls queue context | hold calls queue number | hold calls queue context | agents       |
         | __switchboard-test | __switchboard_hold-test |                 3009 | default               |                    3010 | default                  | 1438@default |
        When I start the XiVO Client
        When I set the switchboard queues:
         | incalls            | on hold                 |
         | __switchboard-test | __switchboard_hold-test |
        When I log in the XiVO Client as "switch", pass "board", logged agent
        When "Alice A" calls "3009"
        When I wait 3 seconds for the call processing
        When the switchboard "Switch Board" selects the incoming call from "Alice A" number "1439"
        When "Switch Board" answers
        Then the switchboard is talking to "Alice A" number "1439"
        When the switchboard "Switch Board" hangs up
        Then the switchboard "Switch Board" is not talking to anyone
        Then "Alice A" is hungup

    Scenario: Hangup sent call not answered
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | number | context | protocol | agent_number |
         | Switch    | Board    | Switchboard | switch    | board      |   1438 | default | sip      |         1438 |
         | Alice     | A        |             |           |            |   1439 | default | sip      |              |
        Given there is a switchboard configured as:
         | incalls queue name | hold calls queue name   | incalls queue number | incalls queue context | hold calls queue number | hold calls queue context | agents       |
         | __switchboard-test | __switchboard_hold-test |                 3009 | default               |                    3010 | default                  | 1438@default |
        When I start the XiVO Client
        When I set the switchboard queues:
         | incalls            | on hold                 |
         | __switchboard-test | __switchboard_hold-test |
        When I log in the XiVO Client as "switch", pass "board", logged agent
        When I dial "1439" with the XiVO Client
        When "Switch Board" answers
        When I wait 3 seconds for the call processing
        Then "Alice A" is ringing
        When the switchboard "Switch Board" hangs up
        Then the switchboard "Switch Board" is not talking to anyone
        Then "Alice A" is hungup

    Scenario: Hangup sent call answered
        Given there are users with infos:
         | firstname | lastname | cti_profile | cti_login | cti_passwd | number | context | protocol | agent_number |
         | Switch    | Board    | Switchboard | switch    | board      |   1438 | default | sip      |         1438 |
         | Alice     | A        |             |           |            |   1439 | default | sip      |              |
        Given there is a switchboard configured as:
         | incalls queue name | hold calls queue name   | incalls queue number | incalls queue context | hold calls queue number | hold calls queue context | agents       |
         | __switchboard-test | __switchboard_hold-test |                 3009 | default               |                    3010 | default                  | 1438@default |
        When I start the XiVO Client
        When I set the switchboard queues:
         | incalls            | on hold                 |
         | __switchboard-test | __switchboard_hold-test |
        When I log in the XiVO Client as "switch", pass "board", logged agent
        When I dial "1439" with the XiVO Client
        When "Switch Board" answers
        When "Alice A" answers
        When I wait 3 seconds for the call processing
        When the switchboard "Switch Board" hangs up
        Then the switchboard "Switch Board" is not talking to anyone
        Then "Alice A" is hungup

Feature: Agent list xlet

    Scenario: Status since indicator changes when an agent logs in
        Given there are users with infos:
         | firstname | lastname | number | agent_number | context | cti_profile | cti_login | cti_passwd | protocol |
         | Jim       | Kirk     | 1110   | 1110         | default | Supervisor  | jim       | kirk       | sip      |
        Given there are queues with infos:
         | name       | display name | number | context | agents_number |
         | enterprise | Enterprise   | 3110   | default | 1110          |
        When I start the XiVO Client
        When I log in the XiVO Client as "jim", pass "kirk"
        Then the agent list xlet shows agent "1110" as unlogged
        When I log agent "1110"
        When I wait 3 seconds for the calls processing
        When I unlog agent "1110"
        When I wait 3 seconds for the calls processing
        Then the agent list xlet shows agent "1110" as unlogged

    Scenario: Status since indicator changes when an agent receives a call from a queue
        Given there are users with infos:
         | firstname | lastname | number | agent_number | context | cti_profile | cti_login | cti_passwd | protocol |
         | Jim       | Kirk     | 1110   | 1110         | default | Supervisor  | jim       | kirk       | sip      |
        Given there are queues with infos:
         | name       | display name | number | context | agents_number |
         | enterprise | Enterprise   | 3110   | default | 1110          |
        Given there is an incall "3110" in context "from-extern" to the "Queue" "enterprise"
        When I start the XiVO Client
        When I log in the XiVO Client as "jim", pass "kirk"
        When I log agent "1110"
        When chan_test calls "3110@from-extern" with id "3110-1"
        When I wait 1 seconds for the calls processing
        When "Jim Kirk" answers
        When I wait 1 seconds for the calls processing
        When "Jim Kirk" hangs up
        When chan_test hangs up "3110-1"
        When chan_test calls "3110@from-extern" with id "3110-1"
        When I wait 1 seconds for the calls processing
        When "Jim Kirk" answers
        When I wait 1 seconds for the calls processing
        Then the agent list xlet shows agent "1110" as in use
        When "Jim Kirk" hangs up
        When chan_test hangs up "3110-1"
        When I wait 1 seconds for the calls processing
        Then the agent list xlet shows agent "1110" as not in use

    Scenario: Status since indicator changes when an agent receives an internal call
        Given there are users with infos:
         | firstname | lastname | number | agent_number | context | cti_profile | cti_login | cti_passwd | protocol |
         | Jim       | Kirk     | 1110   | 1110         | default | Supervisor  | jim       | kirk       | sip      |
         | Spock     | Vulcan   | 1111   |              | default |             |           |            | sip      |
        Given there are queues with infos:
         | name       | display name | number | context | agents_number |
         | enterprise | Enterprise   | 3110   | default | 1110          |
        When I start the XiVO Client
        When I log in the XiVO Client as "jim", pass "kirk"
        When I log agent "1110"
        When chan_test calls "1110@default"
        When I wait 1 seconds for the calls processing
        When "Jim Kirk" answers
        When I wait 1 seconds for the calls processing
        Then the agent list xlet shows agent "1110" as on incoming non-ACD call
        When "Jim Kirk" hangs up
        When I wait 1 seconds for the calls processing
        Then the agent list xlet shows agent "1110" as not in use

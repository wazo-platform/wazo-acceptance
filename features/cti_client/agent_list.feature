Feature: Agent list xlet

    Scenario: Status since indicator changes when an agent logs in
        Given there are users with infos:
         | firstname | lastname | number | agent_number | context | cti_profile | cti_login | cti_passwd |
         | Jim       | Kirk     | 1110   | 1110         | default | Supervisor  | jim       | kirk       |
        Given there are queues with infos:
         | name       | display name | number | context | agents_number |
         | enterprise | Enterprise   | 3110   | default | 1110          |
        When I start the XiVO Client
        When I log in the XiVO Client as "jim", pass "kirk"
        Then the agent list xlet shows agent "1110" as unlogged
        When I log agent "1110"
        Then the agent list xlet shows agent "1110" as not in use
        When I unlog agent "1110"
        Then the agent list xlet shows agent "1110" as unlogged

    Scenario: Status since indicator changes when an agent receives a call from a queue
        Given there are users with infos:
         | firstname | lastname | number | agent_number | context | cti_profile | cti_login | cti_passwd |
         | Jim       | Kirk     | 1110   | 1110         | default | Supervisor  | jim       | kirk       |
        Given there are queues with infos:
         | name       | display name | number | context | agents_number |
         | enterprise | Enterprise   | 3110   | default | 1110          |
        Given there is an incall "3110" in context "from-extern" to the "Queue" "enterprise"
        Given there are no calls running
        When I start the XiVO Client
        When I log in the XiVO Client as "jim", pass "kirk"
        When I log agent "1110"
        Given the agent "1110" will answer a call and hangup after 10 seconds
        When I call extension "3110@from-extern" from trunk "to_incall"
        When I wait 5 seconds
        Then the agent list xlet shows agent "1110" as in use
        When I wait 10 seconds
        Then the agent list xlet shows agent "1110" as not in use

    Scenario: Status since indicator changes when an agent receives an internal call
        Given there are users with infos:
         | firstname | lastname | number | agent_number | context | cti_profile | cti_login | cti_passwd |
         | Jim       | Kirk     | 1110   | 1110         | default | Supervisor  | jim       | kirk       |
         | Spock     | Vulcan   | 1111   |              | default |             |           |            |
        Given there are queues with infos:
         | name       | display name | number | context | agents_number |
         | enterprise | Enterprise   | 3110   | default | 1110          |
        Given there are no calls running
        When I start the XiVO Client
        When I log in the XiVO Client as "jim", pass "kirk"
        When I log agent "1110"
        Given the agent "1110" will answer a call and hangup after 10 seconds
        When I register extension "1111"
        When I call extension "1110@default"
        When I wait 5 seconds
        Then the agent list xlet shows agent "1110" as in use
        When I wait 10 seconds
        Then the agent list xlet shows agent "1110" as not in use

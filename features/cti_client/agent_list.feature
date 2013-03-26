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
        When I log agent "1110"
        Then the agent list xlet shows agent "1110" as not in use
        When I unlog agent "1110"
        Then the agent list xlet shows agent "1110" as unlogged

        #Given there is an incall "3110" in context "from-extern" to the "Queue" "enterprise" with caller id name "starship" "1234"
        #Given there are no calls running

Feature: XIVO Agent

    Scenario: xivo-agentd reconnects when asterisk restarts
        Given there are users with infos:
         | firstname | lastname  | number | context | agent_number |
         | Lord      | Sanderson |   1042 | default | 12345        |
        When I restart "asterisk"
        When I log agent "12345"
        When I unlog agent "12345"
        Then the service "xivo-agent" is running
        Then I see that xivo-agent has reconnected to the AMI in the logs

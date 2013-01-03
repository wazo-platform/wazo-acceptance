Feature: XIVO Agent

    Scenario: xivo-agentd reconnects when asterisk restarts
        Given there is a user "Lord" "Sanderson" with extension "1042@default"
        Given there is a agent "lordsanderson" "" with extension "12345@default"
        When I restart Asterisk
        When I try to log in agent "12345" with extension "1042@default" through xivo-agentctl
        When I try to log off agent "12345" through xivo-agentctl
        Then the service "xivo-agent" is running
        Then I see that xivo-agent has reconnected to the AMI in the logs

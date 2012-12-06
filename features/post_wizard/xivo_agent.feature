Feature: XIVO Agent

    Scenario: xivo-agentd restarts when asterisk goes down
        Given there is a user "Lord" "Sanderson" with extension "1042@default"
        Given there is a agent "lordsanderson" "" with extension "12345@default"
        When I stop Asterisk
        When I try to log in agent "12345" with extension "1042@default" through xivoagentctl
        When I try to log off agent "12345" through xivoagentctl
        Then the service "xivo-agent" is no longer running
        When I wait for the service "xivo-agent" to restart
        Then the service "xivo-agent" is running

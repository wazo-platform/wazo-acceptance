Feature: xivo-agid

    Scenario: Simultaneous agent_get_status AGI requests
        Given there is a agent "John" "Jackson" with number "1001"
        When 10 simultaneous AGI requests are done to get the status of agent 1001
        Then there's no error in xivo-agid log file
        When 10 simultaneous AGI requests are done to get the status of agent 1001
        Then there's no error in xivo-agid log file

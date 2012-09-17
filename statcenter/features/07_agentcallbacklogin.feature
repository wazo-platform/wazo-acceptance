Feature: Stat

    Scenario: Generation of event AGENTCALLBACKLOGIN
        Given there are no calls running
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "007"
        Given there is a user "User" "007" with extension "1007@statscenter"
        Given there is a agent "Agent" "007" with extension "007@statscenter"
        Given I log agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGIN" event for agent "007" in the queue log

    Scenario: Login twice using AGENTCALLBACKLOGIN
        Given there are no calls running
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "007"
        Given there is a user "User" "007" with extension "1007@statscenter"
        Given there is a agent "Agent" "007" with extension "007@statscenter"
        Given I log agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I log agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Then I should see 1 "AGENTCALLBACKLOGIN" event for agent "007" in the queue log

    Scenario: Callid on AGENTCALLBACKLOGIN
        Given there are no calls running
        Given there is no "AGENTCALLBACKLOGIN" entry for agent "007"
        Given there is a user "User" "007" with extension "1007@statscenter"
        Given there is a agent "Agent" "007" with extension "007@statscenter"
        Given I log agent "007" on extension "1007@statscenter"
        Given I wait 5 seconds for the calls processing
        Then the last event "AGENTCALLBACKLOGIN" for agent "007" should not have a callid "NONE"

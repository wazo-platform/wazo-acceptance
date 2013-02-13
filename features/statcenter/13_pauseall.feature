Feature: Stat

    Scenario: Generation of event PAUSEALL and UNPAUSEALL
        Given there are no calls running
        Given there is no agents logged
        Given there is no "UNPAUSEALL" entry for agent "013"
        Given there is a user "User" "013" with extension "1013@statscenter"
        Given there is a agent "Agent" "013" with extension "013@statscenter"
        Given I log agent "013" on extension "1013@statscenter"
        Given I wait 5 seconds for the calls processing
        When I pause agent "013"
        When I unpause agent "013"
        Then I should see 1 "PAUSEALL" event for agent "013" in the queue log
        Then I should see 1 "UNPAUSEALL" event for agent "013" in the queue log

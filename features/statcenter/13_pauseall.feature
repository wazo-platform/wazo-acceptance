Feature: Stat

    Scenario: Generation of event PAUSEALL and UNPAUSEALL
        Given there are no calls running
        Given there is no agents logged
        Given there is no "PAUSEALL" entry for agent "013"
        Given there is no "UNPAUSEALL" entry for agent "013"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 013      |   1013 | statscenter | 013          |
        Given I log agent "013" on extension "1013@statscenter"
        Given I wait 5 seconds for the calls processing
        When I pause agent "013"
        When I unpause agent "013"
        Then I should see 1 "PAUSEALL" event for agent "013" in the queue log
        Then I should see 1 "UNPAUSEALL" event for agent "013" in the queue log

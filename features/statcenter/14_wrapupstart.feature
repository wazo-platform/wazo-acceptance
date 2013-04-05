Feature: Stat

    Scenario: Generation of event WRAPUPSTART
        Given there are no calls running
        Given there is no agents logged
        Given there is no "WRAPUPSTART" entry for agent "014"
        Given there are users with infos:
         | firstname | lastname | number | context     | agent_number |
         | User      | 014      |   1014 | statscenter | 014          |
        Given there are queues with infos:
            | name | number | context     | agents_number | wrapuptime |
            | q14  | 5014   | statscenter | 014           | 15         |
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "014" on extension "1014@statscenter"
        Given I wait 5 seconds for the calls processing
        Given I wait call then i answer then i hang up after "2s"
        Given I wait 2 seconds for the calls processing
        Given there is 1 calls to extension "5014@statscenter" and wait
        Given I wait 9 seconds for the calls processing
        Then i should see 1 "WRAPUPSTART" event for agent "014" in the queue log

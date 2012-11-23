Feature: Stat

    Scenario: Generation of event LEAVEEMPTY
        Given there are no calls running
        Given there is no agents logged
        Given there is no "LEAVEEMPTY" entry in queue "q10"
        Given there is a user "User" "010" with extension "1010@statscenter"
        Given there is a agent "Agent" "010" with extension "010@statscenter"
        Given there is a queue "q10" leaveempty with extension "5010@statscenter" with agent "010"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "010" on extension "1010@statscenter"
        Given I wait 5 seconds for the calls processing
        Given there is 2 calls to extension "5010@statscenter" and wait
        Given I logout agent "010" on extension "1010@statscenter"
        Given I wait 25 seconds for the calls processing
        Then i should see 2 "LEAVEEMPTY" event in queue "q10" in the queue log


Feature: Stat

    Scenario: Generation of event EXITEMPTY
        Given there are no calls running
        Given there is no agents logged
        Given there is no "EXITEMPTY" entry in queue "q13"
        Given there is a user "User" "013" with extension "1013@statscenter"
        Given there is a agent "Agent" "013" with extension "013@statscenter"
        Given there is a queue "q13" leaveempty with extension "5013@statscenter" with agent "013"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "013" on extension "1013@statscenter"
        Given I wait 5 seconds for the calls processing
        Given there is 2 calls to extension "5013@statscenter" and wait
        Given I logout agent "013" on extension "1013@statscenter"
        Given I wait 25 seconds for the calls processing
        Then i should see 2 "EXITEMPTY" event in queue "q13" in the queue log


Feature: Stat

    Scenario: Generation of event RINGNOANSWER
        Given there are no calls running
        Given there is no agents logged
        Given there is no "RINGNOANSWER" entry in queue "q04"
        Given there is a user "User" "004" with extension "1004@statscenter"
        Given there is a agent "Agent" "004" with extension "004@statscenter"
        Given there is a queue "q04" with extension "5004@statscenter" with agent "004"
        Given I wait 5 seconds for the dialplan to be reloaded
        Given I log agent "004" on extension "1004@statscenter"
        Given I wait 5 seconds for the calls processing
        Given there is 1 calls to extension "5004@statscenter" then i hang up after "10s"
        Given I logout agent "004" on extension "1004@statscenter"
        Given I wait 5 seconds for the calls processing
        Then I should see 1 "RINGNOANSWER" event in queue "q04" in the queue log

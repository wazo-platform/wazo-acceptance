Feature: Outcall

    Scenario: Add an outcall
        Given I am logged in
        Given there is no outcall "outdoor"
        Given there is a SIP trunk "door"
        When I create an outcall with name "outdoor" and trunk "door"
        Then there is an outcall "outdoor"

    Scenario: Remove an outcall
        Given I am logged in
        Given there is an outcall "outdoor" with trunk "door"
        When I remove the outcall "outdoor"
        Then there is no outcall "outdoor"

    Scenario: Add an extension in outcall
        Given I am logged in
        Given there is an outcall "outdoor" with trunk "door"
        Given I go to the outcall "outdoor", tab "Exten"
        Given I don't see any exten 7000
        When I go to the outcall "outdoor", tab "Exten"
        When I add an exten
        When I set the exten to 7000
        When I submit
        When I go to the outcall "outdoor", tab "Exten"
        Then I see an exten 7000

    Scenario: Remove an extension in outcall
        Given I am logged in
        Given there is an outcall "outdoor" with trunk "door"
        Given I go to the outcall "outdoor", tab "Exten"
        Given I see an exten 7000
        When I go to the outcall "outdoor", tab "Exten"
        When I remove the exten 7000
        When I submit
        When I go to the outcall "outdoor", tab "Exten"
        Then I don't see any exten 7000
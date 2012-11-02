Feature: Outcall

    Scenario: Add an outcall
        Given there is no outcall "outdoor"
        Given there is a trunksip "door"
        When I create an outcall with name "outdoor" and trunk "door"
        Then outcall "outdoor" is displayed in the list

    Scenario: Remove an outcall
        Given there is no outcall "outdoor"
        Given there is an outcall "outdoor" with trunk "door"
        When I remove the outcall "outdoor"
        Then there is no outcall "outdoor"

    Scenario: Add an extension in outcall
        Given there is no outcall "outdoor"
        Given there is an outcall "outdoor" with trunk "door"
        Given I go to the outcall "outdoor", tab "Exten"
        Given I don't see any exten "7000"
        When I go to the outcall "outdoor", tab "Exten"
        When I add an exten
        When I set the exten to "7000"
        When I submit
        When I go to the outcall "outdoor", tab "Exten"
        Then I see an exten "7000"

    Scenario: Remove an extension in outcall
        Given there is no outcall "outdoor"
        Given there is an outcall "outdoor" with trunk "door"
        Given I go to the outcall "outdoor", tab "Exten"
        Given I see an exten "7000"
        When I go to the outcall "outdoor", tab "Exten"
        When I remove the exten "7000"
        When I submit
        When I go to the outcall "outdoor", tab "Exten"
        Then I don't see any exten "7000"

    Scenario: Edit an outcall and change the context
        Given there is no outcall "linguini"
        Given there is a trunksip "pasta"
        Given there is no context "interco"
        Given there is a outcall context "interco"
        Given there is an outcall "linguini" in context "interco" with trunk "pasta"
        When i edit the outcall "linguini" and set context to "to-extern"
        Then outcall "linguini" is displayed in the list

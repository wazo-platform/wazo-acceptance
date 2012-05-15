Feature: Agent

    Scenario: Add an agent with first name and last name and remove it
        Given I am logged in
        Given I remove agent "23000"
        When I create a agent "Mary" "Stuart" "23000"
        Then agent "Mary Stuart" is displayed in the list of default agent group
        When agent "Mary" "Stuart" is removed
        Then agent "Mary Stuart" is not displayed in the list of default agent group


    Scenario: Agent modification
        Given I am logged in
        Givent an agent "John" "Wayne" "24000" "" in group default
        Then the agent "24000" password is ""
        When I change the agent "24000" password to "8888"
        Then the agent "24000" password is "8888"

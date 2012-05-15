Feature: Agent

    Scenario: Add an agent with first name and last name and remove it
        Given I am logged in
        Given I remove agent "23000"
        When I create a agent "Mary" "Stuart" "23000"
        Then agent "Mary Stuart" is displayed in the list of default agent group
        When agent "Mary" "Stuart" is removed
        Then agent "Mary Stuart" is not displayed in the list of default agent group

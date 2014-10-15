Feature: Agent

    Scenario: Add an agent with first name and last name and remove it
        When I create an agent "Aaliyah" "Stuart" "23000"
        Then agent "Aaliyah Stuart" is displayed in the list of "default" agent group
        When I remove agent "Aaliyah" "Stuart"
        Then agent "Aaliyah Stuart" is not displayed in the list of "default" agent group

    Scenario: Agent modification
        Given there is a agent "John" "Wayne" with extension "24000@default"
        Then the agent "24000" password is ""
        When I change the agent "24000" password to "8888"
        Then the agent "24000" password is "8888"

    Scenario: Agent search
        Given there is a agent "Il" "buono" with extension "24001@default"
        Given there is a agent "Il" "brutto" with extension "24002@default"
        Given there is a agent "Il" "cattivo" with extension "24003@default"
        When I search an agent "24002"
        Then agent "24002" is displayed in the list of "default" agent group
        When I search an agent "cattivo"
        Then agent "cattivo" is displayed in the list of "default" agent group

    Scenario: Agent group
        When I create an agent group "blue"
        Then agent group "blue" is displayed in the list
        When I create an agent "Bisounours" "Red" "24500" in group "blue"
        Then agent "24500" is displayed in the list of "blue" agent group
        Then agent group "blue" has "1" agents
        When I create an agent group "black"
        When I create an agent "bobi" "cash" "26000" in group "black"
        When I create an agent "toto" "bobo" "26001" in group "black"
        Then agent group "black" has "2" agents
        When I remove agent group "blue"
        Then agent group "blue" is not displayed in the list
        When I create an agent group "green"
        Then agent group "green" is displayed in the list
        When I select a list of agent group "black, green"
        When I remove selected agent group
        Then agent group "black" is not displayed in the list
        Then agent group "green" is not displayed in the list

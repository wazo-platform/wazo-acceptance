Feature: Meetme

    Scenario: Add a conference room
        When I add the following conference rooms:
            | name | number |
            | red  | 4000   |
        Then meetme "red" is displayed in the list

    Scenario: Add a conference room with max participants set to 0
        When I add the following conference rooms:
            | name | number | max users |
            | blue | 4000   | 0         |
        Then meetme "blue" is displayed in the list

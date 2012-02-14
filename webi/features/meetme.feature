Feature: Meetme

    Scenario: Add a conference room with max participants set to 0
        Given I am logged in
        When I create a conference room with name "blue" with number "9000" with max participants "0"
        Then conference room "blue" is displayed in the list

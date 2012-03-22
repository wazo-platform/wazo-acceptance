Feature: Line

    Scenario: Add a SIP line and remove it
        Given I am logged in
        When I add a "sip" line
        When I set the context to "default"
        When I submit
        Then this line is displayed in the list
        When I remove this line
        Then this line is not displayed in the list

    Scenario: Add a custom line with 127 characters
        Given I am logged in
        Given there is no custom lines
        When I add a "custom" line
        When I set the interface to "1234567000000000011111111112222222222333333333344444444445555555555666666666677777777778888888888999999999900000000001111111111"
        When I submit
        Then I see no errors

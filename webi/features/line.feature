Feature: Line

    Scenario Outline: Add a SIP line and remove it
        Given I am logged in
        When I create a "SIP" line in context "default"
        Then this line is displayed in the list
        When I remove this line
        Then this line is not displayed in the list

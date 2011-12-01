Feature: Line
    In order to get a line
    I have to create a line

    Scenario Outline: Add a SIP line and remove it
        Given I am logged in
        When I create a SIP line in context default
        Then the list of lines has the lines:
        |identity|protocol|
        |SIP/xxxxxx|SIP|
        When I remove this line
        Then this line is not displayed in the list

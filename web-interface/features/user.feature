Feature: User
    In order to get a user
    I have to create a user

    Scenario: Add a user with first name and last name and remove it
        Given I am logged in
        Given there is no user John Willis
        When I create a user John Willis
        Then user John Willis is displayed in the list
        When user John Willis is removed
        Then user John Willis is not displayed in the list

    Scenario Outline: Add a user in a group
        Given I am logged in
        Given a user Bob Marley in group rastafarien
        When I rename Bob Marley to Bob Dylan
        Then I should be at the user list page
        Then Bob Dylan is in group rastafarien

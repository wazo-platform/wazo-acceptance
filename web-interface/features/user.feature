Feature: User
    In order to get a user
    I have to create a user
        
        
    Scenario Outline: Add a user with first name and last name
        Given I login as root with password superpass at http://192.168.32.195/
        When I create a user John Willis
        Then the list of users has the users:
        |fullName|NbLines|
        |John Willis|0|
        When user is removed
        Then user is not displayed in the list
    
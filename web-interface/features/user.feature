Feature: User
    In order to get a user
    I have to create a user
        
        
    Scenario Outline: Add a user with first name and last name
        Given I login as root with password superpass at http://192.168.32.195/
        Given I create a user John Willis
        Then I see the list of users has the persons:
        |fullName|NbLines|
        |John Willis|0|
    
Feature: User
    In order to get a user
    I have to create a user


    Scenario Outline: Add a user in a group
        Given I login as root with password superpass at http://192.168.32.51/
        Given a user Bob Marley in group rastafarien
        When I rename Bob Marley to Bob Dylan
        Then Bob Dylan is in group rastafarien

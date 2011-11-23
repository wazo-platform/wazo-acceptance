Feature: UserGroup
    In order to get a user with a group
    I have to rename a user with same group

    Scenario Outline: Add a user in a group
        Given I login as root with password superpass at http://skaro-daily.lan-quebec.avencall.com/
        Given a user Bob Marley in group rastafarian
        When I rename Bob Marley to Bob Dylan
        Then I should be at the user list page
        Then Bob Dylan is in group rastafarian

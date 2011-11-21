Feature: Group
    In order to get a group
    I have to create a group

    Scenario Outline: Add a group with name and number and remove it
        Given I login as root with password superpass at http://skaro-daily.lan-quebec.avencall.com/
        Given there is no group with number 5000
        When I create a group Administrative with number 5000
        Then group Administrative is displayed in the list
        When group Administrative is removed
        Then group Administrative is not displayed in the list

Feature: Group
    In order to get a group
    I have to create a group

    Scenario Outline: Add a group with name and number and remove it
        Given I login as root with password superpass at http://skaro-daily.lan-quebec.avencall.com/
        Given there is no group with number 5000
        Given there is no group with name administrative
        When I create a group Administrative with number 5000
        Then group administrative is displayed in the list
        When group administrative is removed
        Then group administrative is not displayed in the list

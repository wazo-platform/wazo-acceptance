Feature: Wizard
    In order to get a working XiVO
    I have to go through the wizard

    Scenario Outline: Successfull completion of the wizard and a login
        Given that there is a XiVO installed at http://192.168.32.170/
        When I start the wizard
        Then I should see the welcome message Bienvenue sur l'installateur de XiVO.
        When I click next
        Then I should be on the licence page
        When I accept the terms of the licence
        When I click next
        Then I should be on the ipbx page
        When I click next
        Then I should be on the DB page

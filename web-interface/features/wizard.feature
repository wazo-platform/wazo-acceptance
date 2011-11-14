Feature: Wizard
    In order to get a working XiVO
    I have to go through the wizard

    Scenario Outline: Successfull completion of the wizard and a login
        Given that there is a XiVO installed at http://192.168.32.242/
        When I start the wizard
        Then I should be on the welcome page
        When I select language en
        Then I should see the welcome message Welcome into the XiVO installer.
        When I click next
        Then I should be on the license page
        When I accept the terms of the licence
        When I click next
        Then I should be on the ipbxengine page
        When I click next
        Then I should be on the dbconfig page
        When I click next
        Then I should be on the checkcomponents page
        When I click next
        Then I should be on the mainconfig page
        When I fill hostname myhostname, domain mydomain, password superpass in the configuration page
        When I click next
        Then I should be on the entitycontext page
        When I fill entity xivo_entity, start 100, end 199
        When I click next
        Then I should be on the ipbximportuser page
        When I click next
        Then I should be on the validate page
        When I click validate
        Then I should be redirected to the login page
        When I login as root with password superpass in en
        Then I should be in the monitoring window

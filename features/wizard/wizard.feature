Feature: Wizard
    In order to get a working XiVO
    I have to go through the wizard

    Scenario: Successfull completion of the wizard and a login
        Given there is XiVO not configured
        When I start the wizard
        Then I should be on the welcome page
        When I select language en
        Then I should see the welcome message Welcome into the XiVO installer.
        When I click next
        Then I should be on the license page
        Then I see the license
        When I accept the terms of the licence
        When I click next
        Then I should be on the mainconfig page
        When I fill hostname skaro-daily, domain lan-quebec.avencall.com, password superpass in the configuration page
        When I click next
        Then I should be on the entitycontext page
        When I fill entity xivo_entity, start 100, end 199
        When I click next
        Then I should be on the validate page
        When I click validate
        Then I should be redirected to the login page
        When I login as root with password superpass in en
        Then I should be logged in "root"

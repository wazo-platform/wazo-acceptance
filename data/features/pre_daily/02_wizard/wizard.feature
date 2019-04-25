Feature: Wizard

    Scenario: Successfull completion of the wizard and create token
        When I pass the setup
        Then I can create an admin token

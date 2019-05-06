Feature: Post Install

    Scenario: Debian sources list points on right mirrors
        Then the mirror list contains a line matching "mirror.wazo.community"

    Scenario: Successfull completion of the wizard and create token
        When I pass the setup
        Then I can create an admin token

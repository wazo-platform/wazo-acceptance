Feature: Setup freshly installed machine

    Scenario: Engine is freshly installed
        Then the mirror list contains a line matching "mirror.wazo.community"

    Scenario: Wizard finishes successfully
        When I pass the setup
        Then I can create an admin token
        Then monit does not monitor the service "isc-dhcp-server"

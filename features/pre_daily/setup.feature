Feature: Setup freshly installed machine

    Scenario: Engine is freshly installed
        Then the mirror list contains a line matching "mirror.wazo.community"
        Then consul returns a running "wazo-setupd" service
    
    Scenario: Wizard is setup successfully when provided with another language
        Given the "asterisk-sounds-wav-fr-fr" Debian package is installed
        When I pass the setup with "fr_FR" as default language
        Then I can create an admin token
        Then monit does not monitor the service "isc-dhcp-server"
        Then the wizard is correctly setup
        Then autoprov endpoint language should be correctly configured as "fr_FR"

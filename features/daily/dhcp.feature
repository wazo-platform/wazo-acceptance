Feature: DHCP server

    Scenario: Enabling DHCP monitors the DHCP server
        When I enable the DHCP feature
        Then monit monitors the service "isc-dhcp-server"
        When I disable the DHCP feature
        Then monit does not monitor the service "isc-dhcp-server"

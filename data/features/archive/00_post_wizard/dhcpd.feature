Feature: DHCPD

    Scenario: DHCP not monitored after wizard executed
        When I wizard correctly executed
        Then I not see "isc-dhcp-server" monitored by monit

    Scenario: DHCP monitored after enable it
        When I activate dhcpd server
        Then I see "isc-dhcp-server" monitored by monit

    Scenario: DHCP not monitored after disable it
        When I desactivate dhcpd server
        Then I not see "isc-dhcp-server" monitored by monit

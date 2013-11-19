Feature: Configuration Files

    Scenario: Add a configuration file
        Given no config file "testlink.conf"
        When I create a configfiles "testlink.conf" with content "[testlink]\n"
        Then configfiles "testlink.conf" is displayed in the list

    Scenario: Add and edit a configuration file without reloading dialplan
        Given no config file "test-no-dialplan-reload.conf"
        When I create a config file "test-no-dialplan-reload.conf" without reloading dialplan
        Then the dialplan has not been reloaded
        When I edit the config file "test-no-dialplan-reload.conf" without reloading dialplan
        Then the dialplan has not been reloaded

    Scenario: Edit a configuration file and reload dialplan
        Given no config file "test-dialplan-reload.conf"
        When I create a config file "test-dialplan-reload.conf" and reload dialplan
        Then the dialplan has been reloaded
        When I edit the config file "test-dialplan-reload.conf" and reload dialplan
        Then the dialplan has been reloaded

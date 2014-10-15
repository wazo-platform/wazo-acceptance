Feature: Configuration Files

    Scenario: Add a configuration file
        Given no config file "testlink.conf"
        When I create a configfiles "testlink.conf" with content "[testlink]\n"
        Then configfiles "testlink.conf" is displayed in the list

    Scenario: Add a configuration file without reloading dialplan
        Given no config file "test-add-no-dialplan-reload.conf"
        Given I watch the log files
        When I create a config file "test-add-no-dialplan-reload.conf" without reloading dialplan
        Then the dialplan has not been reloaded in the log files

    Scenario: Add a configuration file and reload dialplan
        Given no config file "test-add-dialplan-reload.conf"
        Given I watch the log files
        When I create a config file "test-add-dialplan-reload.conf" and reload dialplan
        Then the dialplan has been reloaded in the log files

    Scenario: Edit a configuration file without reloading dialplan
        Given there is a config file "test-edit-no-dialplan-reload.conf"
        Given I watch the log files
        When I edit the config file "test-edit-no-dialplan-reload.conf" without reloading dialplan
        Then the dialplan has not been reloaded in the log files

    Scenario: Edit a configuration file and reload dialplan
        Given there is a config file "test-edit-dialplan-reload.conf"
        Given I watch the log files
        When I edit the config file "test-edit-dialplan-reload.conf" and reload dialplan
        Then the dialplan has been reloaded in the log files

    Scenario: Import a configuration file and reload dialplan
        Given no config file "test-import-dialplan-reload.conf"
        Given I watch the log files
        When I import the config file "test-import-dialplan-reload.conf" and reload dialplan
        Then the dialplan has been reloaded in the log files

    Scenario: Import a configuration file without reloading dialplan
        Given no config file "test-import-no-dialplan-reload.conf"
        Given I watch the log files
        When I import the config file "test-import-no-dialplan-reload.conf" without reloading dialplan
        Then the dialplan has not been reloaded in the log files

    Scenario: Delete a configuration file
        Given there is a config file "test-delete.conf"
        Given I watch the log files
        When I delete the config file "test-delete.conf"
        Then the dialplan has been reloaded in the log files

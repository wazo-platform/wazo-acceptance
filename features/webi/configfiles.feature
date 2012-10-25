Feature: Configuration Files

    Scenario: Add a configuration file
        Given no config file "testlink.conf"
        When I create a configfiles "testlink.conf" with content "[testlink]\n"
        Then configfiles "testlink.conf" is displayed in the list

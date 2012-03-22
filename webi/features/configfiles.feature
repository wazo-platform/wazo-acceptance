Feature: Configuration Files

    Scenario: Add a configuration file
        Given I am logged in
        When I create a configfiles "testlink.conf" with content "[testlink]\n"
        Then configfiles "testlink.conf" is displayed in the list

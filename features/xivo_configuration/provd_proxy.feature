Feature: Provd Proxy

    Scenario: Configure a proxy
        Given I have no proxies configured
        When I configure the following proxies:
          | http proxy              | ftp proxy              | https proxy              |
          | http://example.com:8080 | ftp://example.com:8080 | example.com:8080         |
        When I reload the provisionning general settings page
        When I remove all proxy configurations
        When I reload the provisionning general settings page
        Then there are no proxies configured


Feature: Certificates

    Scenario: Create a certificate with invalid info
        Given there are no certificates named "Cert"
        When I create a certificate with name "Cert" and with email "test@test@test.com" and validity date "10/18/2014"
        When I submit with errors
        When I create a certificate with name "Cert" and with email "test@test.com" and validity date "10/18/2014"
        When I submit
        Then I see no errors

Feature: Certificates

    Scenario: Create a certificate with invalid info
        When I create a certificate with the following invalid info:
          | name | email              | valid date in the future |
          | Cert | test@test@test.com | yes                      |
        Then I see errors
        When I create a certificate with following valid info:
          | name | email         | valid date in the future | autosigned |
          | Cert | test@test.com | yes                      | yes        |
        Then I see no errors

    Scenario: Create a certificate for SIP TLS
        Given I create a certificate with following valid info and the server's hostname as common name:
          | name      | email           | valid date in the future | certificate authority | autosigned |
          | phones    | foo@example.org | yes                      | no                    | yes        |
          | phones-ca | foo@example.org | yes                      | yes                   | yes        |

        When I enable the following options for the SIP Protocol:
          | allow tls connections | listening address | server certificate | ca certificate |
          | yes                   | 0.0.0.0           | phones             | phones-ca      |

        Then SIP tls connections use the "phones" certificate for encryption
        Then there are no warnings when reloading sip configuration


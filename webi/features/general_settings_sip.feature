Feature: SIP General

    Scenario: Global Encryption
        When I enable the SIP encryption option
        Then I should see "encryption" to "yes" in "sip.conf"
        When I disable the SIP encryption option
        Then I should see "encryption" to "no" in "sip.conf"

Feature: IAX general parameters

    Scenario: Toggle Shrink caller ID
        Given the Shrink caller ID option is disabled
        When I enable the Shrink caller ID option
        Then the Shrink caller ID option is enabled
        When I disable the Shrink caller ID option
        Then the Shrink caller ID option is disabled

    Scenario: Toggle SRV lookup
        Given the SRV lookup option is disabled
        When I enable the SRV lookup option
        Then the SRV lookup option is enabled
        When I disable the SRV lookup option
        Then the SRV lookup option is disabled

    Scenario: Add and remove a call limit
        Given the IAX call limit to "10.0.0.1" netmask "255.255.255.255" does not exist
        When I add IAX call limits with errors:
        |  address | netmask | call_count |
        | 10.0.0.1 |         |            |
        Then I see errors
        When I add IAX call limits:
        |  address |         netmask | call_count |
        | 10.0.0.1 | 255.255.255.255 |          1 |
        Then I see IAX call limits:
        |  address |         netmask | call_count |
        | 10.0.0.1 | 255.255.255.255 |          1 |
        When I remove IAX call limits:
        |  address |         netmask | call_count |
        | 10.0.0.1 | 255.255.255.255 |          1 |
        Then I don't see IAX call limits:
        |  address |         netmask | call_count |
        | 10.0.0.1 | 255.255.255.255 |          1 |

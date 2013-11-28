Feature: SCCP General

    Scenario: Enable directmedia
        Given the SCCP directmedia is disabled
        When I enable the SCCP directmedia
        Then the "general" section of "sccp.conf" contains the options:
        | name        | value |
        | directmedia | 1     |
        When I disable the SCCP directmedia
        Then the "general" section of "sccp.conf" contains the options:
        | name        | value |
        | directmedia | 0     |

    Scenario: Change dial timeout
        Given the SCCP dial timeout is at "1" seconds
        When I change the SCCP dial timeout to "6" seconds
        Then the "general" section of "sccp.conf" contains the options:
        | name        | value |
        | dialtimeout | 6     |

    Scenario: Change language
        Given the SCCP language is "en_US"
        When I select the SCCP language "fr_FR"
        Then the "general" section of "sccp.conf" contains the options:
        | name     | value |
        | language | fr_FR |

    Scenario: Customize codecs
        When I customize SCCP codecs to:
        | codec               |
        | G.711 A-law (Audio) |
        | G.729A (Audio)      |
        Then the "general" section of "sccp.conf" contains the options:
        | name     | value      |
        | disallow | all        |
        | allow    | alaw,g729  |
        When I disable SCCP codecs customization
        Then the "general" section of "sccp.conf" does not contain the options:
        | name     |
        | disallow |
        | allow    |

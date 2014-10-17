Feature: General Settings SIP

    Scenario: Global Encryption
        I go on the General Settings > SIP Protocol page, tab "Security"
        When I enable the "Encryption" option
        Then the "general" section of "sip.conf" contains the options:
        | name       | value |
        | encryption | yes   |
        I go on the General Settings > SIP Protocol page, tab "Security"
        When I disable the "Encryption" option
        Then the "general" section of "sip.conf" contains the options:
        | name       | value |
        | encryption | no    |

    Scenario: ISDN compatibility
        I go on the General Settings > SIP Protocol page, tab "Signaling"
        When I enable the "ISDN compatibility (early media)" option
        Then the "general" section of "sip.conf" contains the options:
        | name           | value |
        | prematuremedia | no    |
        I go on the General Settings > SIP Protocol page, tab "Signaling"
        When I disable the "ISDN compatibility (early media)" option
        Then the "general" section of "sip.conf" contains the options:
        | name           | value |
        | prematuremedia | yes   |

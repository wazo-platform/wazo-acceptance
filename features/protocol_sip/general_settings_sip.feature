Feature: General Settings SIP

    Scenario: Global Encryption
        I go on the General Settings > SIP Protocol page, tab "Security"
        When I enable the "Encryption" option
        Then the option "encryption" is at "yes" in "sip.conf"
        I go on the General Settings > SIP Protocol page, tab "Security"
        When I disable the "Encryption" option
        Then the option "encryption" is at "no" in "sip.conf"

    Scenario: ISDN compatibility
        I go on the General Settings > SIP Protocol page, tab "Signaling"
        When I enable the "ISDN compatibility (early media)" option
        Then the option "prematuremedia" is at "no" in "sip.conf"
        I go on the General Settings > SIP Protocol page, tab "Signaling"
        When I disable the "ISDN compatibility (early media)" option
        Then the option "prematuremedia" is at "yes" in "sip.conf"

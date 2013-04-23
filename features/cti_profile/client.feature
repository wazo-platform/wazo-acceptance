Feature: CTI Profile

    Scenario: Start XiVO Client without any services enabled
        Given there is a profile "noservices" with no services and xlets:
        | xlet     |
        | Features |

        Given there are users with infos:
        | firstname | lastname   | cti_profile | cti_login | cti_passwd |
        | Abraham   | Washington | noservices  | abraham   | washington |

        When I start the XiVO Client
        Then I can connect the CTI Client of "Abraham" "Washington"

    Scenario: Edit Xlet list without restart cti server
        Given there is a profile "toto" with no services and xlets:
        | xlet     |
        | Identity |

        Given there are users with infos:
        | firstname | lastname | cti_profile |
        | Al        | Pacino   | toto        | abraham   | washington |

        When I start the XiVO Client
        When I log in the XiVO Client as "al", pass "pacino"
        Then I don't see xlet "datetime"
        When I log out of the XiVO Client
        When I add Xlet "Datetime" to profile "toto"
        When I log in the XiVO Client as "al", pass "pacino"
        Then I see xlet "datetime"
